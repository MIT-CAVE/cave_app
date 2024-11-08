import asyncio, logging, binascii, msgpack, logging, uuid
from redis.asyncio import Redis, ConnectionPool, sentinel

logger = logging.getLogger(__name__)

class PubSubLayer:
    """
    A meta PubSub Layer that uses Redis's pub/sub functionality and allows multiple subscriptions to 
    different channels that may or may not be on different cache shards.

    This layer is designed to be used with asyncio and is not necessarily thread-safe.
    """
    def __init__(
        self,
        hosts=None,
    ):
        """
        Initialize the PubSub Layer

        Requires:
        - hosts: A list of dictionaries
            - Note: This uses a redis connection pool or a sentinel connection pool to connect to the Redis server.
            - Each dictionary should contain the following key value pairs (depending on the connection pool type):
                - ConnectionPool:
                    - address: The address of the Redis server 
                        - EG: 'redis://localhost:6379'
                        - Note: This can be used alone or in conjunction with other connection pool keys
                    - host: The host of the Redis server
                        - Note: This must be used with the port key and can be used in conjunction with the other connection pool keys
                    - port: The port of the Redis server
                        - Note: This must be used with the host key and can be used in conjunction with the other connection pool keys
                    - Other keys listed in the redis-py ConnectionPool documentation
                - SentinelConnectionPool:
                    - master_name: The name of the master in a Redis Sentinel setup
                    - sentinels: A list of sentinel addresses
                    - sentinel_kwargs: A dictionary of keyword arguments to pass to the sentinel connect
                    - Other keys listed in the redis-py SentinelConnectionPool documentation
        """
        self.queue = asyncio.Queue()
        self.subscriptions = dict()
        if not isinstance(hosts, list):
            raise ValueError("Hosts must be a list of dictionaries")
        if len(hosts) == 0:
            raise ValueError("Hosts must contain at least one dictionary")
        self.shards = [ShardConnection(host, self) for host in hosts]
    
    # PubSub methods
    async def subscribe(self, channel:str):
        """
        Subscribe to a channel
        """
        shard = self.__get_shard__(channel)
        if channel not in self.subscriptions:
            self.subscriptions[channel] = shard
        await shard.subscribe(channel)

    async def unsubscribe(self, channel:str):
        """
        Unsubscribe from a channel
        """
        if channel in self.subscriptions:
            shard = self.subscriptions.pop(channel)
            await shard.unsubscribe(channel)

    async def send(self, channel:str, data):
        """
        Send data to a channel
        """
        shard = self.__get_shard__(channel)
        await shard.publish(channel, data)


    async def receive(self) -> dict|None:
        """
        Get the next item from the queue. This will hang until an item is available.

        If the queue has been closed, cleanup and raise an exception to exit the calling task.

        Format:
        {
            'channel': str,
            'data': Any
        }
        """
        try:
            return await self.queue.get()
        except (asyncio.CancelledError, asyncio.TimeoutError, GeneratorExit):
            # Cleanup / unsubscribe on interruptions / exits / timeouts
            await self.flush()
            # Raise an exception to exit the calling task
            raise asyncio.CancelledError

    async def flush(self):
        """
        Flush the layer and close all connections.
        """
        for shard in set(self.subscriptions.values()):
            try:
                await shard.flush()
            except asyncio.CancelledError:
                raise asyncio.CancelledError
            except BaseException as e:
                logger.exception(f"Exception while flushing shard connection: {e}")
        self.subscriptions=dict()


    # Utility Methods
    def __get_shard__(self, channel):
        """
        Return the shard that is used for this channel.

        This is done by assigning a shard index location based on the CRC32 of the channel name.
        """
        if len(self.shards) == 1:
            shard_index = 0
        else:
            hash_val = binascii.crc32(channel.encode("utf8")) & 0xFFF
            shard_index = int(hash_val / (4096 / float(len(self.shards))))
        return self.shards[shard_index]


class ShardConnection:
    def __init__(self, host, pubsub_layer_obj, prefix="pubsub"):
        self.connection_pool = self.__get_connection_pool__(host)
        self.pubsub_layer_obj = pubsub_layer_obj
        self.lock = asyncio.Lock()
        self.connection = None
        self.pubsub = None
        self.receiver_task = None
        self.subscriptions = set()
        self.prefix = prefix

    # PubSub methods
    async def subscribe(self, channel):
        channel = self.__get_channel_name__(channel)
        async with self.lock:
            if channel in self.subscriptions:
                return
            await self.__ensure_connection__()
            await self.pubsub.subscribe(channel)   
            self.subscriptions.add(channel)
        # Drop out of the lock to start the receiver task which requires the lock to be released
        await self.ensure_receiver_task()

    async def unsubscribe(self, channel):
        channel = self.__get_channel_name__(channel)
        async with self.lock:
            if channel not in self.subscriptions:
                return
            await self.__ensure_connection__()
            await self.pubsub.unsubscribe(channel)
            self.subscriptions.remove(channel)
        if len(self.subscriptions) == 0:
            await self.flush()

    async def publish(self, channel, message):
        channel = self.__get_channel_name__(channel)
        async with self.lock:
            await self.__ensure_connection__()
            message = self.__serialize__(message)
            # if the message is larger than 1MB, then save it as a uuid in the same cache and send the uuid
            # This helps bypass the 32 MB limit on pubsub queue size for most cache servers
            # Ensure that this objeect times out after 60s to keep the cache clean
            if len(message) > 1024*1024:
                msg_loc_key = f"{self.prefix}.{str(uuid.uuid4())}"
                await self.connection.set(msg_loc_key, message, ex=60)
                message = self.__serialize__(f'msg:{msg_loc_key}')
            await self.connection.publish(channel, message)

    async def ensure_receiver_task(self):
        async with self.lock:
            if self.receiver_task is None:
                self.receiver_task = asyncio.create_task(self.__receiver_task__())
                # This is needed to continue the main coroutine execution after create_task
                await asyncio.sleep(0)

    async def flush(self):
        # Flushing is not locked since it can be called from inside the lock
        if self.receiver_task:
            self.receiver_task.cancel()
            try:
                await self.receiver_task
            except asyncio.CancelledError:
                pass
            self.receiver_task = None
        if self.pubsub:
            await self.pubsub.close()
            self.pubsub = None
        if self.connection:
            await self.connection.close()
            self.connection = None

    # Tasks
    async def __receiver_task__(self):
        """
        Start a task to receive messages from the pubsub and put them in the queue

        This task will run until all subscriptions are removed.
        
        It will loop continuously as awaiting the pubsub.get_message will not hang the event loop.
        """
        # print("RECEIVER TASK STARTING")
        while len(self.subscriptions) > 0:
            try:
                # Make sure pubsub is active and subscribed otherwise wait for subscription to be established
                if self.pubsub and self.pubsub.subscribed:
                    # Get messages from the pubsub
                    message = await self.pubsub.get_message(ignore_subscribe_messages=True)
                    # If message is not None, put it in the channel queue
                    if message:
                        message_data = self.__deserialize__(message["data"])
                        # If the message was too large, then get that message from the cache
                        if isinstance(message_data, str):
                            if message_data.startswith('msg:'):
                                msg_loc_key = message_data[4:]
                                message_data = self.__deserialize__(await self.connection.get(msg_loc_key))
                        self.pubsub_layer_obj.queue.put_nowait({
                            'channel':self.__get_channel_from_name__(message["channel"].decode()),
                            'data': message_data
                        })
                # Wait for a short time to prevent busy waiting
                # This also serves to wait for the pubsub layer to be subscribed to the channel
                await asyncio.sleep(0.1)
            # Exit on cancellation, timeout, or generator exit (for cleanup afer connection is closed)
            except (asyncio.CancelledError,asyncio.TimeoutError,GeneratorExit):
                # print("RECEIVER TASK KILLED")
                raise asyncio.CancelledError
            except:
                logger.exception("Exception while receiving message from pubsub")
        await self.flush()

    # Utility Methods
    async def __ensure_connection__(self):
        """
        Ensure that the connection to the cache is established.

        Note: This should only be called within a lock.
        """
        if not self.connection:
            self.connection = Redis(connection_pool=self.connection_pool)
            self.pubsub = self.connection.pubsub()
    
    def __get_channel_name__(self, channel):
        """
        Get the channel name with the prefix.
        """
        return f"{self.prefix}.{channel}"
    
    def __get_channel_from_name__(self, channel_name):
        """
        Get the channel name without the prefix.
        """
        return channel_name[len(self.prefix)+1:]
    
    def __serialize__(self, message):
        """
        Serialize a message into bytes.
        """
        return msgpack.packb(message)
    
    def __deserialize__(self, message):
        """
        Deserialize a message from bytes.
        """
        return msgpack.unpackb(message, strict_map_key=False)
    
    @staticmethod
    def __get_connection_pool__(host:dict):
        """
        Get a connection pool from a host dictionary
        """
        host = host.copy()
        if "address" in host:
            address = host.pop("address")
            return ConnectionPool.from_url(address, **host)

        master_name = host.pop("master_name", None)
        if master_name is not None:
            sentinels = host.pop("sentinels")
            sentinel_kwargs = host.pop("sentinel_kwargs", None)
            return sentinel.SentinelConnectionPool(
                master_name,
                sentinel.Sentinel(sentinels, sentinel_kwargs=sentinel_kwargs),
                **host
            )
        return ConnectionPool(**host)
    

