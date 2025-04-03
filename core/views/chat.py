import flet as ft
from core.views.config import Styles
from core.models.models import MessageModel
import traceback


class Chat:
    def __init__(
            self,
            page: ft.Page,
            handle_logout,
            user
        ):
        self.page = page

        self.user = user

        self.btn_logout = ft.FloatingActionButton(
                    icon=ft.Icons.LOGOUT,
                    on_click=handle_logout,
                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS)
            )
        
        self.btn_logout = ft.FloatingActionButton(
                    icon=ft.Icons.LOGOUT,
                    on_click=handle_logout,
                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS)
                )
        
        self.list_messages = ft.ListView(
        expand=True,
        spacing=10,
        height=200,
    )
    
    def update_listview(self):
        # Clear all controls from the list
        self.list_messages.controls.clear()
        self.list_messages.update()

        # Fetch all passwords from the database
        messages = MessageModel.select(user_id=self.user.get_id())

        # Add each password to the list view
        for _, message in enumerate(messages):

            value = ft.Text(
                    f'{message[2]}',
                    size=Styles.MIN_TEXT_SIZE,
                    expand=True,
                    color=ft.Colors.WHITE
                )
            
            message_component = ft.Column([
                ft.Text(
                    f'{message[1]}'.upper(),
                    size=Styles.MID_TEXT_SIZE,
                    color=ft.Colors.WHITE,
                    width=300
                ),
                value,
                ft.Text(
                    f'{message[3]}',
                    size=Styles.MID_TEXT_SIZE,
                    color=ft.Colors.BLACK,
                    width=300
                )
            ])
            self.list_messages.controls.append(message_component)
        self.list_messages.update()