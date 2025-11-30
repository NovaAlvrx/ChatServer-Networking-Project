# server/chat_server.py
import socket
import threading

from client_handler import ClientHandler
from server_core import ServerCore
from utils import (
    color,
    GREEN,
    YELLOW,
    RED,
    CYAN,
    setup_logging,
    log_info,
    log_error,
)


def main():
    HOST = "0.0.0.0"
    PORT = 5002
    MAX_THREADS = 4

    core = ServerCore()
    lock = threading.Lock()

    setup_logging()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(color(f"[SERVER] Listening on {PORT}...", GREEN))
    log_info(f"Server listening on port {PORT}")

    threads: list[threading.Thread] = []

    try:
        while True:
            conn, addr = server_socket.accept()
            print(color(f"[SERVER] Client connected from {addr}", CYAN))
            log_info(f"Client connected from {addr}")

            # Limit thread count
            active_threads = [t for t in threads if t.is_alive()]
            threads = active_threads

            if len(threads) >= MAX_THREADS:
                log_error("Connection rejected: server full")
                print(color("[SERVER] Connection rejected: server full", RED))
                conn.sendall(
                    b'{"type":"event","event":"error","args":{"message":"Server full"}}'
                )
                conn.close()
                continue

            handler = ClientHandler(conn, addr, core, lock)
            handler.start()
            threads.append(handler)

    except KeyboardInterrupt:
        print(color("\n[SERVER] Shutting down via Ctrl-C...", YELLOW))
        log_info("Server shutting down via Ctrl-C")

    finally:
        try:
            server_socket.close()
        except OSError:
            pass
        print(color("[SERVER] Socket closed.", YELLOW))
        log_info("Server socket closed")


if __name__ == "__main__":
    main()
