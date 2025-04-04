import asyncio
import websockets
from core.controller.logger import async_log
import traceback


# List to store connected clients
connected_clients = []


@async_log
async def handle_client(websocket):
    '''
    Handle incoming WebSocket connections and messages.
    '''
    connected_clients.append(websocket)
    print(f"Nuevo cliente conectado: {websocket}.\nTotal: {len(connected_clients)}")

    async for message in websocket:
        print(f"Mensaje recibido: {message}")

        await broadcast(message, websocket)


@async_log
async def broadcast(message, sender_websocket):
    '''
    Broadcast a message to all connected clients except the sender.
    '''
    client_num: int = None
    
    # Find the index of the client sender on the list of clients
    for index, client in enumerate(connected_clients):
        if client == sender_websocket:
            client_num: int = index + 1
            break

    message_to_send = f"Usuario {client_num}: {message}"

    # list to store tasks
    tasks: list = []

    # Send the message to all clients except the sender
    for client in connected_clients:
        if client == sender_websocket:
            continue
        try:
            tasks.append(client.send(message_to_send))
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Error - Cliente desconectado: {e}")
            connected_clients.remove(client)

    # Wait for all tasks to complete
    await asyncio.gather(*tasks, return_exceptions=True)


@async_log
async def server():
    '''
    Server Starter function.
    '''
    async with websockets.serve(
        handle_client, 
        "localhost", 
        8000,
        ping_interval=20,
        ping_timeout=60,):
        print("Servidor WebSocket iniciado en ws://localhost:8000")
        await asyncio.Future()