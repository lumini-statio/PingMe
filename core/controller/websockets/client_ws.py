import asyncio
import websockets
import flet as ft
from plyer import notification
from datetime import datetime

from core.models.models import MessageModel, UserModel
from core.models.user.user import User
from core.controller.notif_manager import NotificationManager
from core.controller.logger import async_log, log


class WebSocketClient:
    def __init__(self, page: ft.Page, user: User, update_listview):
        self.page = page
        self.user = user
        self.update_listview = update_listview
        self.websocket = None
        self.running = False
        self.receive_task = None
        self.lock = asyncio.Lock()


    @async_log
    async def connect(self):
        """
        fun that connect the client to the server
        """
        uri = "ws://localhost:8080"
        try:
            await self.disconnect()

            notification_manager = NotificationManager()
            
            async with self.lock:
                self.websocket = await websockets.connect(
                    uri,
                    ping_interval=20,
                    ping_timeout=60,
                )
                
                self.running = True

                # add client as notifications observer
                notification_manager.add_observer(self.websocket)

                # start the receive task to listen for messages
                self.receive_task = asyncio.create_task(self.receive_messages())

        except Exception:
            await self.reconnect()


    @async_log
    async def send_message(self, message):
        """
        Fun to send messages to the server
        """
        # if the message is empty, dont send it
        if not message.strip():
            return

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        async with self.lock:
            # check if the client is connected, else reconnect
            if self.websocket is None:
                await self.reconnect()
                return

            try:
                """
                create an instance in db of the message sent,
                send it to the server and update the messages listview
                """
                MessageModel.create(
                    message=message,
                    sender=self.user.id,
                    time_sent=now
                )
                
                await self.websocket.send(f"{self.user.username}-{message}-{now}")
                
                await self.update_listview()

            except Exception:
                await self.reconnect()


    @async_log
    async def receive_messages(self):
        """
        Fun that receives info from the server
        and update the view
        """
        while self.running:
            try:
                async with self.lock:
                    try:
                        # check if the client is connected, else reconnect
                        if self.websocket is None:
                            await self.reconnect()
                            continue

                        message = await asyncio.wait_for(
                            self.websocket.recv(),
                            timeout=1.0
                        )

                        msg_parts = message.split(sep='-')

                        await self.update_listview()

                        self.send_notification(
                            client_name = f'{msg_parts[0]}',
                            message = f'{msg_parts[1]}'
                        )

                    except asyncio.TimeoutError:
                        continue

            except websockets.exceptions.ConnectionClosed:
                await self.reconnect()
                break


            except Exception:
                await asyncio.sleep(0.5)
    

    @staticmethod
    @log
    def send_notification(client_name: str, message: str):

        notification.notify(
            title=f'{client_name}',
            message=message,
            timeout=5,
            app_name='chat'
        )


    @async_log
    async def reconnect(self):
        """
        fun that reconnect the client to the server
        """
        if not self.running:
            return
            
        async with self.lock:
            await self.disconnect()
            await asyncio.sleep(3)
            await self.connect()


    @async_log
    async def disconnect(self):
        """
        fun that disconnect the client to the server
        """
        async with self.lock:
            self.running = False
            
            # cancel the task if its running
            if self.receive_task and not self.receive_task.done():
                self.receive_task.cancel()

                try:
                    await self.receive_task
                    
                except (asyncio.CancelledError, Exception):
                    pass

                self.receive_task = None
            
            # close clients connection
            if self.websocket is not None:
                try:
                    await self.websocket.close()

                except Exception:
                    pass

                self.websocket = None
