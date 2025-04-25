from contextlib import closing
from config import SERVER_PORT
import socket


def is_port_in_use(*args) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(1)
            return sock.connect_ex(('localhost', SERVER_PORT)) == 0