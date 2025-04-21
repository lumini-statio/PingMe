import asyncio
import websockets
from core.controller.utils.logger import async_log
from config import SERVER_PORT
from contextlib import closing
import socket



class WebSocketServer:
    def __init__(self):
        self.connected_clients = []
        self.stop_event = asyncio.Event()
    

    @async_log
    async def handle_client(self, websocket):
        '''
        Handle incoming websockets connections and messages.
        '''
        self.connected_clients.append(websocket)

        async for message in websocket:
            await self.broadcast(message, websocket)


    @async_log
    async def broadcast(self, message, sender_websocket):
        '''
        Broadcast a message to all connected clients except the sender.
        '''
        message_to_send = f"{message}"

        tasks: list = []

        # send the message to all clients connected except the sender
        for client in self.connected_clients:
            if client == sender_websocket:
                continue
            try:
                tasks.append(client.send(message_to_send))
            except websockets.exceptions.ConnectionClosed as e:
                self.connected_clients.remove(client)

        await asyncio.gather(*tasks, return_exceptions=True)


    @async_log
    async def server(self):
        '''
        Server Starter function.
        '''
        async with websockets.serve(
            self.handle_client, 
            "0.0.0.0", 
            SERVER_PORT,
            ping_interval=20,
            ping_timeout=60):

            await self.stop_event.wait()

            await asyncio.Future()


    def is_port_in_use(*args) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(1)
            return sock.connect_ex(('localhost', SERVER_PORT)) == 0
    

    def run_server(self):
        if not self.is_port_in_use():
            try:
                asyncio.run(self.server())
            finally:
                self.stop_event.set()