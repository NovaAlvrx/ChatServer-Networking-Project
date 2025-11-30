# client/receiver_thread.py
import threading

from protocol import parse_message

# === Color constants ===
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}"


class ReceiverThread(threading.Thread):
    """
    Background listener for server events so they print as soon as they arrive.
    """

    def __init__(self, sock):
        super().__init__(daemon=True)
        self.sock = sock
        self.running = True

    def stop(self) -> None:
        self.running = False
        try:
            self.sock.shutdown(1)
        except OSError:
            pass

    def run(self) -> None:
        while self.running:
            try:
                data = self.sock.recv(1024)
            except OSError:
                break

            if not data:
                print(color("\n[CLIENT] Disconnected from server.", YELLOW))
                break

            event = parse_message(data)
            if event:
                self._display(event)

    def _display(self, event: dict) -> None:
        etype = event.get("event")
        args = event.get("args", {})

        if etype == "message":
            channel = args.get("channel", "?")
            sender = args.get("from_user", "Unknown")
            text = args.get("text", "")
            print(color(f"\n[{channel}] {sender}: {text}", GREEN))

        elif etype == "joined":
            print(color(f"\n[CLIENT] Joined {args.get('channel')}", CYAN))

        elif etype == "left":
            print(color(f"\n[CLIENT] Left {args.get('channel')}", YELLOW))

        elif etype == "list":
            print(color(f"\n[CLIENT] Channels: {args.get('channels')}", MAGENTA))

        elif etype == "nick_set":
            print(color(f"\n[CLIENT] Nickname set to {args.get('nickname')}", CYAN))

        elif etype == "goodbye":
            print(color("\n[CLIENT] Server closed connection.", YELLOW))
            self.running = False

        else:
            print(color(f"\n[SERVER EVENT]: {event}", YELLOW))
