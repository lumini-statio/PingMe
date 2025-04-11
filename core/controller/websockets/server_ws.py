import asyncio
import websockets
from core.controller.utils.logger import async_log
from config import SERVER_PORT


# List to store connected clients
connected_clients = []


@async_log
async def handle_client(websocket):
    '''
    Handle incoming websockets connections and messages.
    '''
    connected_clients.append(websocket)

    async for message in websocket:
        await broadcast(message, websocket)


@async_log
async def broadcast(message, sender_websocket):
    '''
    Broadcast a message to all connected clients except the sender.
    '''
    message_to_send = f"{message}"

    tasks: list = []

    for client in connected_clients:
        if client == sender_websocket:
            continue
        try:
            tasks.append(client.send(message_to_send))
        except websockets.exceptions.ConnectionClosed as e:
            connected_clients.remove(client)

    await asyncio.gather(*tasks, return_exceptions=True)


@async_log
async def server():
    '''
    Server Starter function.
    '''
    async with websockets.serve(
        handle_client, 
        "localhost", 
        SERVER_PORT,
        ping_interval=20,
        ping_timeout=60):

        await asyncio.Future()