import json, asyncio, logging
from .broadcaster import Broadcaster
from .utils import run_in_thread

logger = logging.getLogger(__name__)

class BaseSocketServer(Broadcaster):
    def __init__(self, scope, receive, send):
        self.__scope__ = scope
        self.__receive__ = receive
        self.__send__ = send
        self.is_alive = True
        super().__init__()

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
        asyncio.run_coroutine_threadsafe(self.__async_send__(data), self.__loop__)

    # Async Functions
    async def __async_send__(self, data:[dict|list|str|float|int]):
        """
        Send data to the websocket client. 
        - Note: In general, this should not be called directly, but data should be broadcasted 
                and handled by __broadcast_listener_task__ instead

        Requires:

        - data: [dict|list|str|float|int] = The data to send to the client
            - Note: This data must be JSON serializable
        """
        try:
            json_data = json.dumps(data)
        except:
            raise ValueError("Data must be JSON serializable")
        await self.__send__({'type': 'websocket.send', 'text': json_data})

    # Tasks
    async def __ws_listener_task(self):
        """
        Listen for incoming WS data and handle it accordingly        
        """
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
                channel, data = await self.async_receive_broadcast()
                await self.__async_send__(data)
            
    # Lifecycle Methods
    def __kill__(self):
        """
        Kill the socket server and stop all tasks
        """
        self.is_alive = False
    
    # Utility Methods
    @classmethod
    def as_asgi(cls):
        """
        Return an ASGI application that can be run by daphne or other ASGI servers

        This method is a class method so that it can be called as a pure function by an un-instantiated 
        class which is required by the daphne server
        """
        async def app(scope, receive, send):
            # Wrap in a try / except block to catch unclean exits handled by Daphne
            try:
                # Initialize the socket server object
                socket_server = cls(scope, receive, send)
                # Create Tasks for the listener and queue processor
                ws_listener_task = asyncio.create_task(socket_server.__ws_listener_task())
                broadcast_listener_task = asyncio.create_task(socket_server.__broadcast_listener_task__())
                # wait until the socket server is killed or the tasks are cancelled
                while socket_server.is_alive:
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
        return app

    # Placeholder Methods
    def receive(self, data):
        """
        Placeholder method for the receive method that must be overwritten by the user
        """
        raise NotImplementedError("The receive method must be implemented by the user")
    
    def connect(self):
        """
        Placeholder method for the connect method that can be overwritten by the user.
        """
        pass