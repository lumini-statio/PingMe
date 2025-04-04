import asyncio
import websockets
import flet as ft
from core.models.models import MessageModel, UserModel
from core.models.user.user import User
from datetime import datetime


class WebSocketClient:
    def __init__(self, page: ft.Page, user: User, update_listview):
        self.page = page
        self.user = user
        self.update_listview = update_listview
        self.websocket = None
        self.running = False

    async def connect(self):
        uri = "ws://localhost:8000"
        try:
            self.websocket = await websockets.connect(
                uri,
                ping_interval=20,
                ping_timeout=60,
            )
            self.running = True
            asyncio.create_task(self.receive_messages())
            print("Conectado al servidor WebSocket")
        except Exception as e:
            print(f"Error de conexión: {e}")
            await self.page.show_snack_bar(
                ft.SnackBar(ft.Text("Error al conectar con el servidor"), open=True)
            )

    async def send_message(self, message):
        now = datetime.now().time().strftime('%DD - %H:%M')
        if self.websocket:
            try:
                MessageModel.create(
                    message=message,
                    sender=self.user.model,
                    time_sent=now
                )
                
                await self.websocket.send(f"{now} - {self.user.username}:{message}")
                
                # Actualizar la vista
                await self.update_listview()
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
                await self.reconnect()

    async def receive_messages(self):
        while self.running:
            try:
                if self.websocket:
                    message = await self.websocket.recv()
                    print(f"Mensaje recibido: {message}")
                        
                    await self.update_listview()
                        
            except websockets.exceptions.ConnectionClosed:
                print("Conexión cerrada, reconectando...")
                await self.reconnect()
            except Exception as e:
                print(f"Error al recibir mensajes: {e}")
                await asyncio.sleep(1)

    async def reconnect(self):
        await self.disconnect()
        await asyncio.sleep(3)
        await self.connect()

    async def disconnect(self):
        self.running = False
        if self.websocket:
            await self.websocket.close()


# async def send_messages(websocket):
#     '''
#     Send messages to the WebSocket server.
#     '''
#     print("Escribe 'exit' para salir")
#     while True:
#         message = await ainput("")
#         await websocket.send(message)
#         if message.lower() == 'exit':
#             break


# async def receive_messages(websocket):
#     '''
#     Receive messages from the WebSocket server.
#     '''
#     while True:
#         try:
#             message = await websocket.recv()
#             print(f"\n{message}")
#         except websockets.exceptions.ConnectionClosed:
#             print("Reconectando en 3 segundos...")
#             await asyncio.sleep(3)


# async def main():
#     '''
#     Main function to connect to the WebSocket server and handle messages.
#     '''
#     async with websockets.connect(
#         "ws://localhost:8000",
#         ping_interval=20,
#         ping_timeout=60,
#         ) as websocket:
#         print("Conectado al servidor WebSocket. Escribe 'exit' para salir.")
        
#         # Create tasks for sending and receiving messages
#         sender = asyncio.create_task(send_messages(websocket))
#         receiver = asyncio.create_task(receive_messages(websocket))
        
#         await asyncio.gather(sender, receiver)


# if __name__ == '__main__':
#     asyncio.run(main())
