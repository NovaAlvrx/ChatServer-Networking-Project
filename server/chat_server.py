import socket

def main():
    HOST = "0.0.0.0"
    PORT = 5001

    print(f"[SERVER] Starting on port {PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("[SERVER] Waiting for a client...")
    conn, addr = server_socket.accept()
    print(f"[SERVER] Client connected from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("[CLIENT SAID]:", data.decode())
        conn.sendall(b"Message received")

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()