from core.views.app import main_view
# from core.controller.websockets.server_ws import WebSocketServer

import flet as ft
import threading


if __name__ == '__main__':

    # sv = WebSocketServer()

    # threading.Thread(target=sv.run_server, daemon=True).start()
    ft.app(target=main_view)
