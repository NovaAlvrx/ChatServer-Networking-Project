import threading
from protocol import parse_message, make_event

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, core, lock):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.core = core
        self.lock = lock
        self.running = True

        # Default nickname
        self.core.set_nick(conn, "Unknown")

    def run(self):
        print(f"[THREAD] Started for {self.addr}")

        while self.running:
            try:
                data = self.conn.recv(1024)
                if not data:
                    break

                obj = parse_message(data)
                if not obj:
                    continue

                self.handle_command(obj)

            except ConnectionResetError:
                break

        print(f"[THREAD] Closing connection for {self.addr}")
        self.conn.close()

    # ==== Command handling ====

    def handle_command(self, obj):
        cmd = obj["command"]

        if cmd == "nick":
            nickname = obj["args"]["nickname"]
            with self.lock:
                self.core.set_nick(self.conn, nickname)
            self.conn.sendall(make_event("nick_set", nickname=nickname))

        elif cmd == "join":
            channel = obj["args"]["channel"]
            with self.lock:
                self.core.join_channel(self.conn, channel)

            self.conn.sendall(make_event("joined", channel=channel))

        elif cmd == "leave":
            channel = obj["args"].get("channel")
            with self.lock:
                if channel:
                    self.core.leave_channel(self.conn, channel)
                else:
                    # leave all channels
                    channels = self.core.get_user_channels(self.conn)
                    for ch in channels:
                        self.core.leave_channel(self.conn, ch)

            self.conn.sendall(make_event("left", channel=channel))

        elif cmd == "list":
            chans = self.core.list_channels()
            self.conn.sendall(make_event("list", channels=chans))

        elif cmd == "message":
            text = obj["args"]["text"]
            nickname = self.core.get_nick(self.conn)

            channels = self.core.get_user_channels(self.conn)
            for ch in channels:
                msg = make_event("message", channel=ch, from_user=nickname, text=text)
                with self.lock:
                    self.core.broadcast(ch, msg)

        elif cmd == "quit":
            self.conn.sendall(make_event("goodbye"))
            self.running = False

        else:
            self.conn.sendall(make_event("error", message="Unknown command"))