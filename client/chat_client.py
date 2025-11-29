import socket
from receiver_thread import ReceiverThread
from protocol import make_command

def main():
    HOST = "127.0.0.1"
    PORT = 5001

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print("[CLIENT] Connected.")
    print("Commands: /nick, /join, /leave, /list, /quit")

    # Start background listener so server events show up immediately
    receiver = ReceiverThread(client_socket)
    receiver.start()
    
    while True:
        user_input = input("> ").strip()

        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0][1:]

            if cmd == "nick":
                msg = make_command("nick", nickname=parts[1])

            elif cmd == "join":
                msg = make_command("join", channel=parts[1])

            elif cmd == "leave":
                if len(parts) > 1:
                    msg = make_command("leave", channel=parts[1])
                else:
                    msg = make_command("leave")

            elif cmd == "list":
                msg = make_command("list")

            elif cmd == "quit":
                msg = make_command("quit")
                client_socket.sendall(msg)
                receiver.stop()
                break

            else:
                print("[CLIENT] Unknown command")
                continue

        else:
            # normal chat message
            msg = make_command("message", text=user_input)

        client_socket.sendall(msg)

    client_socket.close()
    receiver.join()

if __name__ == "__main__":
    main()
