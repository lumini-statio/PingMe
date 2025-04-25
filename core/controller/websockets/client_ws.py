import asyncio
import websockets
import flet as ft
import threading
from plyer import notification
from datetime import datetime

from core.models.models import MessageModel, UserModel
from core.models.user.entity import User
from core.controller.utils.notif_manager import NotificationManager
from core.controller.utils.server_status import is_port_in_use
from core.controller.utils.logger import async_log, log
from core.controller.websockets.server_ws import WebSocketServer
from config import SERVER_PORT


class WebSocketClient:
    def __init__(self, page: ft.Page, user: User, update_listview):
        self.page = page
        self.user = user
        self.update_listview = update_listview
        self.websocket = None
        self.running = False
        self.receive_task = None
        self._lock = None
        self.server = WebSocketServer()


    @property
    async def lock(self):
        if self._lock is None:
            self._lock = asyncio.Lock()
        
        return self._lock

    @async_log
    async def connect(self):
        """
        fun that connect the client to the server
        """
        uri = f"ws://localhost:{SERVER_PORT}"
        try:
            await self.disconnect()

            notification_manager = NotificationManager()
            
            async with (await self.lock):
                self.websocket = await websockets.connect(
                    uri,
                    ping_interval=20,
                    ping_timeout=60,
                    open_timeout=5,
                    close_timeout=1
                )

                print(f'Connected to {uri}')
                
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

        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')

        if not is_port_in_use():
            threading.Thread(
                target=self.server.run_server,
                daemon=True
            ).start()

            asyncio.sleep(0.2)

            await self.connect()

        async with (await self.lock):
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
                
                await self.websocket.send(
                    f'{self.user.username}-{message}-{now}',
                    text=True
                )
                
                await self.update_listview()

            except Exception:
                await self.reconnect()


    @async_log
    async def receive_messages(self):
        """
        Fun that receives info from the server
        and update the view
        """
        if not is_port_in_use():
            threading.Thread(
                target=self.server.run_server,
                daemon=True
            ).start()

            asyncio.sleep(0.2)

            await self.connect()
        
        while self.running:
            try:
                async with (await self.lock):
                    # check if the client is connected, else reconnect
                    if self.websocket is None:
                        await self.reconnect()
                        continue
                    
                    # recieve the message from server
                    message = await asyncio.wait_for(
                        self.websocket.recv(),
                        timeout=1.0
                    )

                    msg_parts = message.split(sep='-')

                    if 'DELETE' in msg_parts[0]:
                        await MessageModel.delete_by_id(int(msg_parts[1]))

                        return

                    sender_name = msg_parts[0]
                    message_text = msg_parts[1]
                    sent = msg_parts[2]

                    sender = UserModel.get_or_none(
                        UserModel.username == sender_name
                    )

                    if not sender:
                        return
                    
                    message_exists = MessageModel.select()\
                        .where(
                        (MessageModel.sender == sender.id) &
                        (MessageModel.message == message_text) &
                        (MessageModel.time_sent == sent)
                    ).exists()

                    if not message_exists:
                        MessageModel.create(
                            message = message_text,
                            sender = sender.id,
                            time_sent = sent
                        )

                    await self.update_listview()

                    self.send_notification(
                        client_name = f'{sender_name}',
                        message = f'{message_text}'
                    )


            except websockets.exceptions.ConnectionClosed:
                threading.Thread(
                    target=self.server.run_server,
                    daemon=True
                ).start()

                await self.connect()
                break


            except (asyncio.TimeoutError, Exception):
                await asyncio.sleep(0.2)
                continue
    

    @async_log
    async def delete_message(self, message_id):
        try:
            MessageModel.delete_by_id(int(message_id))
            await self.update_listview()
            await self.send_message(f'DELETE-{message_id}')

        except Exception:
            pass


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
        if not is_port_in_use():
            threading.Thread(
                target=self.server.run_server,
                daemon=True
            ).start()

            asyncio.sleep(0.2)

            await self.connect()

        if not self.running:
            return
            
        async with (await self.lock):
            await self.disconnect()
            await asyncio.sleep(0.5)
            await self.connect()
        


    @async_log
    async def disconnect(self):
        """
        fun that disconnect the client to the server
        """
        if is_port_in_use()\
        and self._lock is not None:
            
            async with (await self.lock):
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

                    except (Exception):
                        pass

                    self.websocket = None
