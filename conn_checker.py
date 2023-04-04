import socket


socket_address = ("www.google.com", 80)

async def get_connection_status():
    """Сокет проверяет наличие соединения и возвращает boolean value"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM):
        try:
            socket.create_connection(socket_address, timeout=1.0)
            return True
        except Exception:
            return False
