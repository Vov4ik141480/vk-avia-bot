import socket


def check_connection():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except Exception as exc:
        return False


check_connection()