import flet as ft
from core.views.config import Styles
from core.models.user.user import User
from core.views.enter import Enter
from core.views.chat import Chat
from core.controller.logger import log
import traceback


class Main:
    def __init__(
            self,
            page: ft.Page
        ):
        self.page = page
        self.page.title = 'Chat in network'
        self.page.window.width = 1000
        self.page.window.height = 700
        self.page.padding = 0
        self.page.bgcolor = ft.Colors.WHITE10
        self.page.theme_mode = ft.ThemeMode.LIGHT

        self.page.theme = Styles.PAGE_THEME.value

        self.user = User()
        self.enter_page = Enter(
            page=page,
            user=self.user,
            handle_logout=self.handle_logout
        )
        self.chat_page = Enter(
            page=self.page,
        )

        self.content_area = ft.Container(
            content=self.enter_page.login_view,
            expand=True
        )


    def update_view(self):
        """
        If the user is authenticated change the view
        to the password generator, if not, returns
        to the login view
        """
        try:
            if self.user.is_authenticated():
                self.content_area.content = self.chat_page.view
            else:
                self.content_area.content = self.enter_page.login_view
            self.page.update()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    

    def handle_logout(self, e):
        try:
            self.enter_page.username_field.value = ''
            self.enter_page.login_password_field.value = ''
            self.user.state.change_user_state(
                user=self.user
                )
            self.update_view()
        except Exception as e:
            log(f'{__file__} - {traceback.format_exc()}')
    
    def run(self):
        self.page.add(ft.Container(
            content=self.content_area,
            expand=True,
            bgcolor=ft.Colors.WHITE24,
            padding=0,
            alignment=ft.alignment.center
        ))