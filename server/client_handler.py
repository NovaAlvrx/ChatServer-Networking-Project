# server/client_handler.py
import threading

from protocol import parse_message, make_event
from server_core import ServerCore
from utils import log_info, log_error


class ClientHandler(threading.Thread):
    """
    One thread per connected client. Receives JSON command objects
    from the client, updates ServerCore, and sends JSON event objects
    back to the client.
    """

    def __init__(self, conn, addr, core: ServerCore, lock: threading.Lock):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.core = core
        self.lock = lock
        self.running = True

        # Default nickname
        self.core.set_nick(self.conn, "Unknown")

    def run(self) -> None:
        log_info(f"Handler started for {self.addr}")
        try:
            while self.running:
                try:
                    data = self.conn.recv(1024)
                except ConnectionResetError:
                    break

                if not data:
                    break

                obj = parse_message(data)
                if not obj:
                    continue

                self.handle_command(obj)

        finally:
            # Clean up server state and close socket
            with self.lock:
                self.core.remove_conn(self.conn)
            self.conn.close()
            log_info(f"Connection closed for {self.addr}")

    # ------------------------------------------------------------------
    # Command handling
    # ------------------------------------------------------------------

    def handle_command(self, obj: dict) -> None:
        cmd = obj.get("command")
        args = obj.get("args", {})

        if cmd == "nick":
            nickname = args.get("nickname", "Unknown")
            self.core.set_nick(self.conn, nickname)
            self.conn.sendall(make_event("nick_set", nickname=nickname))
            log_info(f"Nick set for {self.addr}: {nickname}")

        elif cmd == "join":
            channel = args.get("channel", "?")
            self.core.join_channel(self.conn, channel)
            self.core.broadcast(
                channel,
                make_event("joined", channel=channel),
            )
            log_info(f"{self.addr} joined channel {channel}")

        elif cmd == "leave":
            channel = args.get("channel")

            if channel:
                self.core.leave_channel(self.conn, channel)
                self.core.broadcast(
                    channel,
                    make_event("left", channel=channel),
                )
                log_info(f"{self.addr} left channel {channel}")
            else:
                # Leave all channels this user is in
                channels = self.core.get_user_channels(self.conn)
                for ch in channels:
                    self.core.leave_channel(self.conn, ch)
                    self.core.broadcast(
                        ch,
                        make_event("left", channel=ch),
                    )
                log_info(f"{self.addr} left all channels")

        elif cmd == "list":
            chans = self.core.list_channels()
            self.conn.sendall(make_event("list", channels=chans))
            log_info(f"Sent channel list to {self.addr}")

        elif cmd == "message":
            text = args.get("text", "")
            nickname = self.core.get_nick(self.conn)
            channels = self.core.get_user_channels(self.conn)

            for ch in channels:
                msg = make_event(
                    "message",
                    channel=ch,
                    from_user=nickname,
                    text=text,
                )
                self.core.broadcast(ch, msg)

            log_info(f"{nickname} ({self.addr}) said '{text}' in channels {channels}")

        elif cmd == "quit":
            self.conn.sendall(make_event("goodbye"))
            self.running = False
            log_info(f"{self.addr} requested quit")

        else:
            self.conn.sendall(make_event("error", message="Unknown command"))
            log_error(f"Unknown command from {self.addr}: {cmd}")
