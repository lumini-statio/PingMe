import asyncio
import websockets
from aioconsole import ainput


async def send_messages(websocket):
    '''
    Send messages to the WebSocket server.
    '''
    print("Escribe 'exit' para salir")
    while True:
        message = await ainput("")
        await websocket.send(message)
        if message.lower() == 'exit':
            break


async def receive_messages(websocket):
    '''
    Receive messages from the WebSocket server.
    '''
    while True:
        try:
            message = await websocket.recv()
            print(f"\n{message}")
        except websockets.exceptions.ConnectionClosed:
            print("Reconectando en 3 segundos...")
            await asyncio.sleep(3)


async def main():
    '''
    Main function to connect to the WebSocket server and handle messages.
    '''
    async with websockets.connect(
        "ws://localhost:8000",
        ping_interval=20,
        ping_timeout=60,
        ) as websocket:
        print("Conectado al servidor WebSocket. Escribe 'exit' para salir.")
        
        # Create tasks for sending and receiving messages
        sender = asyncio.create_task(send_messages(websocket))
        receiver = asyncio.create_task(receive_messages(websocket))
        
        await asyncio.gather(sender, receiver)


if __name__ == '__main__':
    asyncio.run(main())
