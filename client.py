# client.py
"""
ChatClient - Requirement 3

Simple text-based chat client.
- Takes NO command-line arguments.
- User connects via: /connect <host> [port]
- Uses object-based JSON protocol defined in protocol.py
"""

import socket
import threading
from typing import Optional


from protocol import (
    send_obj,
    recv_obj_from_file,
    cmd_nick,
    cmd_list,
    cmd_join,
    cmd_leave,
    cmd_quit,
    cmd_message,
)


DEFAULT_PORT = 5000


class ChatClient:
    def __init__(self):
        self.sock: Optional[socket.socket] = None
        self.sock_file = None  # file-like wrapper for reading lines
        self.current_channel: Optional[str] = None
        self.running = True

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    def connect(self, host: str, port: int = DEFAULT_PORT) -> None:
        if self.sock:
            print("[INFO] Already connected. Use /quit to disconnect first.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            # Wrap the socket in a file for line-based reading
            self.sock_file = self.sock.makefile("r", encoding="utf-8")
            print(f"[INFO] Connected to {host}:{port}")

            # Start background thread to receive messages
            t = threading.Thread(target=self._receiver_loop, daemon=True)
            t.start()
        except OSError as e:
            print(f"[ERROR] Could not connect: {e}")
            self.sock = None
            self.sock_file = None

    def disconnect(self) -> None:
        self.running = False
        try:
            if self.sock_file:
                self.sock_file.close()
            if self.sock:
                self.sock.close()
        except OSError:
            pass
        finally:
            self.sock = None
            self.sock_file = None
            print("[INFO] Disconnected from server.")

    # ------------------------------------------------------------------
    # Sending / receiving
    # ------------------------------------------------------------------

    def _send(self, obj: dict) -> None:
        if not self.sock:
            print("[WARN] Not connected. Use /connect <host> [port].")
            return
        try:
            send_obj(self.sock, obj)
        except OSError as e:
            print(f"[ERROR] Failed to send message: {e}")
            self.disconnect()

    def _receiver_loop(self) -> None:
        """
        Runs in a background thread, continuously reading objects from the server
        and printing them in a human-readable form.
        """
        while self.running and self.sock_file:
            try:
                obj = recv_obj_from_file(self.sock_file)
            except OSError:
                obj = None

            if obj is None:
                print("[INFO] Server closed the connection.")
                self.disconnect()
                break

            self._handle_incoming(obj)

    def _handle_incoming(self, obj: dict) -> None:
        msg_type = obj.get("type")
        action = obj.get("action")

        if msg_type == "event":
            if action == "message":
                ch = obj.get("channel")
                nick = obj.get("nickname")
                text = obj.get("text")
                print(f"[{ch}] {nick}: {text}")
            elif action == "user_joined":
                ch = obj.get("channel")
                nick = obj.get("nickname")
                print(f"[{ch}] * {nick} joined the channel")
            elif action == "user_left":
                ch = obj.get("channel")
                nick = obj.get("nickname")
                print(f"[{ch}] * {nick} left the channel")
            elif action == "list":
                channels = obj.get("data", {}).get("channels", [])
                print("Channels:")
                for ch in channels:
                    print(f"  {ch['name']} ({ch['users']} users)")
            elif action == "notice":
                print(f"[NOTICE] {obj.get('text')}")
            elif action == "nick_ok":
                print(f"[INFO] Nickname set to {obj.get('nickname')}")
            else:
                print(f"[EVENT] {obj}")

        elif msg_type == "error":
            print(f"[SERVER ERROR] {action}: {obj.get('text')}")

        else:
            print(f"[UNKNOWN] {obj}")

    # ------------------------------------------------------------------
    # REPL: read-eval-print loop for user input
    # ------------------------------------------------------------------

    def repl(self) -> None:
        print("=== ChatClient ===")
        print("Commands:")
        print("  /connect <host> [port]")
        print("  /nick <name>")
        print("  /join <channel>")
        print("  /leave [channel]")
        print("  /list")
        print("  /quit")
        print("  /help")
        print("Anything else is sent as a message to the current channel.\n")

        while self.running:
            try:
                line = input("> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n[INFO] Exiting client...")
                # Try to tell server we're quitting
                if self.sock:
                    self._send(cmd_quit())
                break

            if not line:
                continue

            if line.startswith("/"):
                self._handle_command(line)
            else:
                # Regular chat message
                if not self.current_channel:
                    print("[WARN] Join a channel first with /join <channel>.")
                    continue
                self._send(cmd_message(self.current_channel, line))

        # Cleanup
        if self.sock:
            self.disconnect()

    def _handle_command(self, line: str) -> None:
        parts = line.split()
        cmd = parts[0].lower()

        if cmd == "/connect":
            if len(parts) < 2:
                print("Usage: /connect <host> [port]")
                return
            host = parts[1]
            port = int(parts[2]) if len(parts) >= 3 else DEFAULT_PORT
            self.connect(host, port)

        elif cmd == "/nick":
            if len(parts) < 2:
                print("Usage: /nick <name>")
                return
            self._send(cmd_nick(parts[1]))

        elif cmd == "/join":
            if len(parts) < 2:
                print("Usage: /join <channel>")
                return
            channel = parts[1]
            self.current_channel = channel
            self._send(cmd_join(channel))

        elif cmd == "/leave":
            # Optional channel name
            channel = parts[1] if len(parts) >= 2 else self.current_channel
            self._send(cmd_leave(channel))

        elif cmd == "/list":
            self._send(cmd_list())

        elif cmd == "/quit":
            self._send(cmd_quit())
            self.running = False

        elif cmd == "/help":
            print("Commands:")
            print("  /connect <host> [port]")
            print("  /nick <name>")
            print("  /join <channel>")
            print("  /leave [channel]")
            print("  /list")
            print("  /quit")
            print("  /help")

        else:
            print(f"[WARN] Unknown command: {cmd}. Try /help.")


def main() -> None:
    client = ChatClient()
    client.repl()


if __name__ == "__main__":
    main()
