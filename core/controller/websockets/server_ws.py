import asyncio
import websockets
import socket

from core.controller.utils.server_status import is_port_in_use
from core.controller.utils.logger import async_log, log
from config import SERVER_PORT


class WebSocketServer:
    def __init__(self):
        self.connected_clients = []
        self.stop_event = asyncio.Event()
        self.sock = None

    @async_log
    async def handle_client(self, websocket):
        '''
        Handle incoming websockets connections and messages.
        '''
        self.connected_clients.append(websocket)

        try:
            async for message in websocket:
                await self.broadcast(message, websocket)
        
        except Exception as e:
            print(e)


    @async_log
    async def broadcast(self, message, sender_websocket):
        '''
        Broadcast a message to all connected clients except the sender.
        '''
        tasks: list = []

        # send the message to all clients connected except the sender
        for client in self.connected_clients:
            if client == sender_websocket:
                continue
            try:
                tasks.append(client.send(message))
            except websockets.exceptions.ConnectionClosed as e:
                self.connected_clients.remove(client)

        await asyncio.gather(*tasks, return_exceptions=True)


    @async_log
    async def server(self):
        '''
        Server Starter function.
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", SERVER_PORT))
        self.sock.listen()

        async with websockets.serve(
            self.handle_client, 
            sock=self.sock,
            ping_interval=20,
            ping_timeout=60,
            close_timeout=10
            ):
            
            print(f'Running server on port {SERVER_PORT}')

            await self.stop_event.wait()

            await asyncio.Future()
    

    @log
    def run_server(self):
        if not is_port_in_use():
            try:
                asyncio.run(self.server())
            finally:
                self.stop_event.set()