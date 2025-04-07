import asyncio
import websockets
from core.controller.logger import async_log
import traceback


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
    client_num: int = None
    
    for index, client in enumerate(connected_clients):
        if client == sender_websocket:
            client_num: int = index + 1
            break

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
        8080,
        ping_interval=20,
        ping_timeout=60):

        await asyncio.Future()