import flet as ft
from core.views.config import Styles
from core.models.user.user import User
from core.views.enter import auth_view
from core.views.chat import chat_view
from core.controller.logger import log
import traceback
import asyncio


async def main_view(page: ft.Page):
    page.title = 'Chat in network'
    page.window_center()
    page.window.resizable = False
    page.window.maximizable = False
    page.window_width = Styles.PAGE_WIDTH.value
    page.window_height = Styles.PAGE_HEIGHT.value
    page.padding = 0
    page.bgcolor = ft.Colors.PRIMARY
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = Styles.PAGE_THEME.value

    user = User()
    current_view = None

    async def update_view():

        nonlocal current_view

        page.controls.clear()
        page.overlay.clear()

        if user.is_authenticated():

            chat_components = chat_view(page, user, update_view)

            current_view = chat_components["view"]
            page.add(current_view)

            await chat_components["update_listview"]()
        else:
            auth_components = auth_view(page, user, update_view)
            current_view = auth_components["view"]
            page.overlay.append(auth_components["dialog"])
            page.add(current_view)

        await page.update_async()

    await update_view()
