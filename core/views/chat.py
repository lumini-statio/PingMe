import flet as ft
from core.views.config import Styles
from core.models.models import MessageModel
from core.models.user.user import User
import traceback
import asyncio


def chat_view(page: ft.Page, user: User, update_view):
    list_messages = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True,
    )

    async def handle_logout(e):
        user.state.change_user_state(user)
        await update_view()

    btn_logout = ft.FloatingActionButton(
        icon=ft.icons.LOGOUT,
        on_click=handle_logout,
        shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS),
        visible=True
    )

    msg_input = ft.TextField(
        expand=False,
        height=60,
        bgcolor=Styles.BG_COLOR,
        border_color=Styles.BORDER_COLOR,
        hint_text='Type your message',
    )

    async def update_listview():
        list_messages.controls.clear()
        
        example_messages = [
            ("System", "Welcome to the chat!", "10:00 AM"),
            ("User1", "Hello everyone!", "10:05 AM"),
            ("User2", "Hi there!", "10:06 AM")
        ]
        
        for sender, message, time in example_messages:
            message_component = ft.Container(
                content=ft.Column([
                    ft.Text(sender, size=Styles.MID_TEXT_SIZE, color=ft.Colors.WHITE),
                    ft.Text(message, size=Styles.MIN_TEXT_SIZE, color=ft.Colors.WHITE),
                    ft.Text(time, size=Styles.MID_TEXT_SIZE, color=ft.Colors.BLUE_100)
                ]),
                bgcolor=ft.Colors.BLUE_900,
                padding=10,
                border_radius=5
            )
            list_messages.controls.append(message_component)
        
        await list_messages.update_async()

    return {
        "view": ft.Container(
            content=ft.Column([
                btn_logout,
                ft.Container(
                    content=list_messages,
                    bgcolor=ft.colors.BLUE_GREY_900,
                    border_radius=5,
                    padding=10,
                    expand=True,
                ),
                msg_input,
            ], expand=True),
            padding=10,
            expand=True
        ),
        "update_listview": update_listview
    }
