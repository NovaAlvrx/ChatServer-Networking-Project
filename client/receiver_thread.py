import threading
from protocol import parse_message


class ReceiverThread(threading.Thread):
    """
    Background listener for server events so they print as soon as they arrive.
    """

    def __init__(self, sock):
        super().__init__(daemon=True)
        self.sock = sock
        self.running = True

    def stop(self):
        self.running = False
        try:
            self.sock.shutdown(1)
        except OSError:
            pass

    def run(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
            except OSError:
                break

            if not data:
                print("\n[CLIENT] Disconnected from server.")
                break

            event = parse_message(data)
            if event:
                self._display(event)

    def _display(self, event):
        etype = event.get("event")
        args = event.get("args", {})

        if etype == "message":
            channel = args.get("channel", "?")
            sender = args.get("from_user", "Unknown")
            text = args.get("text", "")
            print(f"\n[{channel}] {sender}: {text}")
        elif etype == "joined":
            print(f"\n[CLIENT] Joined {args.get('channel')}")
        elif etype == "left":
            print(f"\n[CLIENT] Left {args.get('channel')}")
        elif etype == "list":
            print(f"\n[CLIENT] Channels: {args.get('channels')}")
        elif etype == "nick_set":
            print(f"\n[CLIENT] Nickname set to {args.get('nickname')}")
        elif etype == "goodbye":
            print("\n[CLIENT] Server closed connection.")
            self.running = False
        else:
            print(f"\n[SERVER EVENT]: {event}")
