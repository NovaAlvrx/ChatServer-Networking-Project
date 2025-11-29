import socket
import threading
from client_handler import ClientHandler
from server_core import ServerCore

def main():
    HOST = "0.0.0.0"
    PORT = 5002
    MAX_THREADS = 4

    core = ServerCore()
    lock = threading.Lock()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"[SERVER] Listening on {PORT}...")

    threads = []

    while True:
        conn, addr = server_socket.accept()
        print(f"[SERVER] Client connected from {addr}")

        # Limit thread count
        active_threads = [t for t in threads if t.is_alive()]
        threads = active_threads

        if len(threads) >= MAX_THREADS:
            conn.sendall(
                b'{"type":"event","event":"error","args":{"message":"Server full"}}'
            )
            conn.close()
            continue

        handler = ClientHandler(conn, addr, core, lock)
        handler.start()
        threads.append(handler)

if __name__ == "__main__":
    main()