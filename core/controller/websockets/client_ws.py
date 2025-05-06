import asyncio
import websockets
import flet as ft
import threading
import ssl
from plyer import notification
from datetime import datetime

from core.models.models import MessageModel, UserModel
from core.models.user.entity import User
from core.controller.utils.notif_manager import NotificationManager
from core.controller.utils.server_status import is_port_in_use
from core.controller.utils.logger import async_log, log
# from core.controller.websockets.server_ws import WebSocketServer
from config import SERVER_PORT, WS_SERVER
import asyncio
import websockets
import flet as ft
import ssl
from plyer import notification
from datetime import datetime

class WebSocketClient:
    def __init__(self, page: ft.Page, user: User, update_listview):
        self.page = page
        self.user = user
        self.update_listview = update_listview
        self.websocket = None
        self.running = False
        self.receive_task = None
        self._lock = asyncio.Lock()
        self.uri = WS_SERVER
        self.ssl_context = ssl.create_default_context()

    async def ensure_connection(self):
        async with self._lock:
            if self.websocket is None or self.websocket.closed:
                await self.connect()

    async def connect(self):
        await self.disconnect()  # Asegurarse de limpiar conexiones anteriores
        
        try:
            self.websocket = await websockets.connect(
                self.uri,
                ping_interval=20,
                ping_timeout=60,
                open_timeout=5,
                close_timeout=1,
                ssl=self.ssl_context
            )
            
            self.running = True
            self.receive_task = asyncio.create_task(self.receive_messages())
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(1)
            return False

    async def send_message(self, message):
        if not message.strip():
            return

        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        
        await self.ensure_connection()

        try:
            MessageModel.create(
                message=message,
                sender=self.user.id,
                time_sent=now
            )
            
            await self.websocket.send(f'{self.user.username}-{message}-{now}')
            await self.update_listview()
        except Exception as e:
            print(f"Send error: {e}")
            await self.reconnect()

    async def receive_messages(self):
        while self.running:
            try:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=1.0)
                await self.process_received_message(message)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Receive error: {e}")
                await self.reconnect()
                break

    async def process_received_message(self, message):
        msg_parts = message.split('-')
        
        if 'DELETE' in msg_parts[0]:
            await MessageModel.delete_by_id(int(msg_parts[1]))
            return

        sender_name, message_text, sent = msg_parts[0], msg_parts[1], msg_parts[2]
        
        sender = UserModel.get_or_none(UserModel.username == sender_name)
        if not sender:
            return
        
        if not MessageModel.select().where(
            (MessageModel.sender == sender.id) &
            (MessageModel.message == message_text) &
            (MessageModel.time_sent == sent)
        ).exists():
            MessageModel.create(
                message=message_text,
                sender=sender.id,
                time_sent=sent
            )

        await self.update_listview()
        self.send_notification(client_name=sender_name, message=message_text)

    async def reconnect(self):
        if not self.running:
            return
            
        await self.disconnect()
        await asyncio.sleep(1)
        await self.connect()

    async def disconnect(self):
        self.running = False
        
        if self.receive_task:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except:
                pass
            self.receive_task = None
            
        if self.websocket:
            try:
                await self.websocket.close()
            except:
                pass
            self.websocket = None

    @staticmethod
    def send_notification(client_name: str, message: str):
        notification.notify(
            title=f'{client_name}',
            message=message,
            timeout=5,
            app_name='chat'
        )
