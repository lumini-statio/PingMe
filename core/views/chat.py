import flet as ft
from config import Styles
from core.models.models import MessageModel, UserModel
from core.models.user.entity import User
from core.controller.websockets.client_ws import WebSocketClient
from core.controller.utils.logger import log, async_log


@log
def chat_view(page: ft.Page, user: User, update_view):
    list_messages = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    
    @async_log
    async def update_listview():
        list_messages.controls.clear()

        messages = (
            MessageModel
            .select(MessageModel, UserModel)
            .join(UserModel, on=(MessageModel.sender == UserModel.id))
            .order_by(MessageModel.time_sent)
        )
        

        for message in messages:
            time = str(message.time_sent).replace('T', ' ')
            is_current_user = message.sender.username == user.username
            message_component = ft.Container(
                content=ft.Column([
                    ft.Text(
                        'Tú' if is_current_user else message.sender.username,
                        size=Styles.MIN_TEXT_SIZE.value,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        message.message,
                        size=Styles.MID_TEXT_SIZE.value,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        time,
                        color=ft.Colors.WHITE,
                        italic=True,
                    )
                ]),
                bgcolor=ft.Colors.BLACK12 if not is_current_user else ft.Colors.BLUE_900,
                padding=10,
                border_radius=10,
                margin=5,
            )
            list_messages.controls.append(message_component)
        
        list_messages.update()


    @async_log
    async def handle_send_message(e):
        if msg_input.value.strip():
            await ws_client.send_message(msg_input.value)
            msg_input.value = ""
            msg_input.update()

    # Inicializar el cliente WebSocket después de definir handle_send_message
    ws_client = WebSocketClient(page, user, update_listview)


    @async_log
    async def handle_logout(e):
        await ws_client.disconnect()
        user.state.change_user_state(user)
        await update_view()


    @async_log
    async def load_chat():
        await update_listview()
        await ws_client.connect()

    # Ahora define los controles que usan las funciones
    btn_logout = ft.FloatingActionButton(
        icon=ft.Icons.LOGOUT,
        on_click=handle_logout,
        shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS),
        visible=True
    )

    msg_input = ft.TextField(
        width=610,
        bgcolor=Styles.BG_COLOR.value,
        border_color=Styles.BORDER_COLOR.value,
        border_radius=Styles.BTN_RADIUS.value,
        hint_text='Type your message',
        on_submit=handle_send_message,
        multiline=True,
        shift_enter=True,
        max_length=1000,
        text_size=Styles.MIN_TEXT_SIZE.value,
    )

    btn_send = ft.FloatingActionButton(
        icon=ft.Icons.SEND,
        shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS.value),
        width=45,
        height=45,
        visible=True,
        on_click=handle_send_message
    )

    return {
        "view": ft.Container(
            content=ft.Column([
                btn_logout,
                ft.Container(
                    content=list_messages,
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                ft.Row([
                    msg_input,
                    btn_send
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                )
            ], 
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            expand=True,
        ),
        "load_chat": load_chat,
        "disconnect": ws_client.disconnect,
    }
