import socket

def main():
    HOST = "127.0.0.1"
    PORT = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("[CLIENT] Connected to server.")
    while True:
        msg = input("> ")
        client_socket.sendall(msg.encode())
        reply = client_socket.recv(1024)
        print("[SERVER]:", reply.decode())

if __name__ == "__main__":
    main()