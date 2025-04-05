import flet as ft
from core.views.app import main_view
from core.controller.websockets.server_ws import server
import threading
import socket
import asyncio
from contextlib import closing

def is_port_in_use(port: int) -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        return sock.connect_ex(('localhost', port)) == 0

def run_server():
    if not is_port_in_use(8080):
        asyncio.run(server())

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    ft.app(target=main_view)