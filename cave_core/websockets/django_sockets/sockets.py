import json, asyncio, logging
from .broadcaster import Broadcaster
from .utils import run_in_thread

logger = logging.getLogger(__name__)

class BaseSocketServer(Broadcaster):
    def __init__(self, scope, receive, send, config=None):
        """
        Initialize the socket server

        Required:

        - scope: dict = The scope of the websocket connection
        - receive: method = The `get` method for an asyncio.Queue() object that will be used to receive data from the websocket client
        - send: async callable = The function that should send the data to the websocket client
            - Note: This function takes in a dictionary with the following keys:
                - type: str = The type of message to send (always 'websocket.send')
                - text: str = The data to send to the client (the json serialized version of the data sent / broadcasted)
        
        Optional:
                
        - config: dict = The configuration for the socket server
            - hosts: list = A list of dictionaries that contain the host information for the socket server
                - See: django_sockets.pubsub.PubSubLayer docs for more more comprehensive docs on the config parameter
            - Default: 
                - If provided in django settings: settings.DJANGO_SOCKETS_CONFIG
                - Else: {'hosts': [{'address': 'redis://localhost:6379'}]}
        """
        self.scope = scope
        self.__receive__ = receive
        self.__send__ = send
        self.is_alive = True
        super().__init__(config=config)

    # Sync Functions
    def send(self, data:[dict|list|str|float|int]):
        """
        Send data to the websocket client. 
        - Note: This only sends data to the client from which the calling function was called
        - Note: To send data to all clients that are subscribed to a channel, use the broadcast method
                which is inherited from the Broadcaster class

        Requires:

        - data: [dict|list|str|float|int] = The data to send to the client
            - Note: This data must be JSON serializable
        """
        self.run_async(self.async_send(data))

    def run_async(self, func):
        """
        Run an async function in the current object's event loop
        """
        asyncio.run_coroutine_threadsafe(func, self.__loop__)

    # Async Functions
    async def async_send(self, data:[dict|list|str|float|int]):
        """
        Send data to the websocket client. 
        - Note: To send data to all clients that are subscribed to a channel, use the broadcast method
                which is inherited from the Broadcaster class

        Requires:

        - data: [dict|list|str|float|int] = The data to send to the client
            - Note: This data must be JSON serializable
        """
        if self.__send__ is None:
            logger.log(logging.ERROR, "The send and async_send functions are not available because the send parameter was not provided when the socket server was initialized. To silence this warning, you can provide a function that simulates some sending behavior.")
        else:
            try:
                json_data = json.dumps(data)
            except:
                raise ValueError("Data must be JSON serializable")
            await self.__send__({'type': 'websocket.send', 'text': json_data})

    async def async_handle_received_broadcast(self, channel:str, data:[dict|list|str|float|int]):
        """
        Handle a received broadcast from a subscribed channel

        This method is provided so that it can be overwritten by the user if they want to handle
        received broadcasts from subscriptions in a specific way.

        By default, this method will send the data to the client using the async_send method

        In general, this method should only be called by the __broadcast_listener_task__ method

        Requires:

        - channel: str = The channel that the data was broadcasted to
        - data: [dict|list|str|float|int] = The data that was broadcasted
            - Note: This data must be JSON serializable
        """
        await self.async_send(data)

    # Tasks
    async def __ws_listener_task__(self):
        """
        Listen for incoming WS data and handle it accordingly        
        """
        if self.__receive__ is None:
            logger.log(logging.ERROR, "The websocket listener task is not available because the receive parameter was not provided when the socket server was initialized. To silence this warning, you can provide an asyncio.Queue() receive parameter and put items in it to simulate received ws messages.")
        else:
            while self.is_alive:
                data = await self.__receive__()
                if data['type'] == 'websocket.receive':
                    try:
                        data_text = json.loads(data['text'])
                        run_in_thread(self.receive, data_text)
                    except:
                        logger.exception("Invalid JSON data received")
                elif data['type'] == 'websocket.disconnect':
                    self.__kill__()
                elif data['type'] == 'websocket.connect':
                    await self.__send__({'type': 'websocket.accept'})
                    self.connect()
                else:
                    raise ValueError(f"Invalid WS data type: {data['type']}")

    async def __broadcast_listener_task__(self):
        """
        Handle all messages that were broadcast to subscribed channels
        """
        # Only handle broadcasts if the broadcaster is usable
        if self.__usable__:
            while self.is_alive:
                try:
                    channel, data = await self.async_receive_broadcast()
                    await self.async_handle_received_broadcast(channel, data)
                # Cleanup on exit
                except asyncio.CancelledError:
                    raise asyncio.CancelledError
                except Exception as e:
                    raise e
            
    # Lifecycle Methods
    def __kill__(self):
        """
        Kill the socket server and stop all tasks
        """
        self.is_alive = False

    async def async_start_listeners(self):
        try:
            # Create Tasks for the listener and queue processor
            ws_listener_task = asyncio.create_task(self.__ws_listener_task__())
            broadcast_listener_task = asyncio.create_task(self.__broadcast_listener_task__())
            # wait until the socket server is killed or the tasks are cancelled
            while self.is_alive:
                await asyncio.sleep(0.2)
        # Catch exits handled by Daphne and allow the tasks to be cancelled
        except asyncio.CancelledError:
            pass
        # Ensure all tasks are cancelled
        ws_listener_task.cancel()
        broadcast_listener_task.cancel()
        # Allow the cancelation to run in the background
        # The next line allows the async function to return
        # and the above tasks to be cancelled in the background
        await asyncio.sleep(0)

    def start_listeners(self):
        """
        Start the listeners for the socket server
        """
        self.run_async(self.async_start_listeners())

    # Utility Methods
    @classmethod
    async def as_asgi(cls, scope, receive, send):
        """
        An ASGI application runner function that can be called by Daphne.

        This creates a new socket server instance and starts the listeners in the background.
        """
        # Wrap in a try / except block to catch unclean exits handled by Daphne
        socket_server = cls(scope, receive, send)
        await socket_server.async_start_listeners()

    # Placeholder Methods
    def receive(self, data):
        """
        Placeholder method for the receive method that must be overwritten by the user

        This is the method that will be called when data is received from the ws client.
        """
        raise NotImplementedError("The receive method must be implemented by the user")
    
    def connect(self):
        """
        Placeholder method for the connect method that can be overwritten by the user.
        """
        pass