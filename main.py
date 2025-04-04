import flet as ft
from core.views.app import main_view
from core.controller.websockets.server_ws import server
import asyncio
import threading


def run_server():
    asyncio.run(server())

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    ft.app(target=main_view)