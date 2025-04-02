import flet as ft
from core.views.config import Styles
import traceback


class Chat:
    def __init__(
            self,
            page: ft.Page,
            handle_logout,
        ):
        self.page = page

        self.btn_logout = ft.FloatingActionButton(
                    icon=ft.Icons.LOGOUT,
                    on_click=handle_logout,
                    shape=ft.RoundedRectangleBorder(radius=Styles.BTN_RADIUS)
                )