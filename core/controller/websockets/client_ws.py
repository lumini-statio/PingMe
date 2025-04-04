import asyncio
import websockets
from websockets import ClientConnection
import flet as ft
from core.models.models import MessageModel
from core.models.user.user import User
from datetime import datetime
from core.controller.logger import async_log


class WebSocketClient:
    def __init__(self, page: ft.Page, user: User, update_listview):
        self.page = page
        self.user = user
        self.update_listview = update_listview
        self.websocket = None
        self.running = False
        self.receive_task = None
        self.lock = asyncio.Lock()  # Para evitar condiciones de carrera

    @async_log
    async def connect(self):
        uri = "ws://localhost:8000"
        try:
            await self.disconnect()  # Limpia cualquier conexión previa
            
            async with self.lock:
                self.websocket = await websockets.connect(
                    uri,
                    ping_interval=20,
                    ping_timeout=60,
                )
                self.running = True
                self.receive_task = asyncio.create_task(self.receive_messages())
        except Exception as e:
            await self.page.show_snack_bar(
                ft.SnackBar(ft.Text("Error al conectar con el servidor"), open=True)
            )
            await self.reconnect()

    @async_log
    async def send_message(self, message):
        if not message.strip():
            return

        now = datetime.now().strftime('%H:%M')
        async with self.lock:
            if self.websocket is None:
                await self.reconnect()
                return

            try:
                MessageModel.create(
                    message=message,
                    sender=self.user.id,
                    time_sent=now
                )
                
                await self.websocket.send(f"{now} - {self.user.username}:{message}")
                
                await self.update_listview()
            except Exception as e:
                await self.reconnect()

    @async_log
    async def receive_messages(self):
        while self.running:
            try:
                async with self.lock:
                    if self.websocket is None:
                        await asyncio.sleep(1)
                        continue

                    try:
                        message = await asyncio.wait_for(
                            self.websocket.recv(),
                            timeout=1.0
                        )
                        await self.update_listview()
                    except asyncio.TimeoutError:
                        continue
                        
            except websockets.exceptions.ConnectionClosed as e:
                await self.reconnect()
                break
            except Exception as e:
                await asyncio.sleep(1)

    @async_log
    async def reconnect(self):
        if not self.running:
            return
            
        async with self.lock:
            await self.disconnect()
            await asyncio.sleep(3)
            await self.connect()

    @async_log
    async def disconnect(self):
        async with self.lock:
            self.running = False
            
            # Cancela la tarea de recepción
            if self.receive_task and not self.receive_task.done():
                self.receive_task.cancel()
                try:
                    await self.receive_task
                except (asyncio.CancelledError, Exception):
                    pass
                self.receive_task = None
            
            # Cierra la conexión WebSocket
            if self.websocket is not None:
                try:
                    await self.websocket.close()
                except Exception:
                    pass
                self.websocket = None
