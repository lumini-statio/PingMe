import asyncio
import websockets
import keyboard


async def send_messages(websocket):
    while True:
        message = input("Tú: ")
        await websocket.send(message)
        if message.lower() == 'exit':
            break

async def receive_messages(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(f"\nRecibido: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Conexión cerrada por el servidor")
            break

async def main():
    async with websockets.connect("wss://localhost:8002") as websocket:
        print("Conectado al servidor WebSocket. Escribe 'exit' para salir.")
        
        # Ejecutar sender y receiver en paralelo
        sender = asyncio.create_task(send_messages(websocket))
        receiver = asyncio.create_task(receive_messages(websocket))
        
        await asyncio.gather(sender, receiver)


if __name__ == '__main__':
    asyncio.run(main())

# async def start_client():
#     async with websockets.connect('ws://localhost:8002') as websocket:
#         done = False
#         while not done:
#             if keyboard.is_pressed('space'):
#                 await websocket.send('buzz')
#                 message = await websocket.recv()
#                 print(message)
#                 done = True


# if __name__ == '__main__':
#     asyncio.run(start_client())
