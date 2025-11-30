# client/chat_client.py
import socket
from typing import Optional

from receiver_thread import ReceiverThread
from protocol import make_command


DEFAULT_PORT = 5002


class ChatClient:
    """
    Text-based chat client for the group chat server.

    - Takes NO command-line arguments.
    - User connects with: /connect <host> [port]
    - Uses JSON object protocol via protocol.make_command()
    """

    def __init__(self) -> None:
        self.sock: Optional[socket.socket] = None
        self.receiver: Optional[ReceiverThread] = None
        self.running: bool = True

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    def connect(self, host: str, port: int = DEFAULT_PORT) -> None:
        if self.sock is not None:
            print("[CLIENT] Already connected. Use /quit to disconnect first.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            print(f"[CLIENT] Connected to {host}:{port}.")

            # Start background listener so server events show up immediately
            self.receiver = ReceiverThread(self.sock)
            self.receiver.start()
        except OSError as e:
            print(f"[CLIENT] Could not connect: {e}")
            self.sock = None
            self.receiver = None

    def disconnect(self) -> None:
        """Cleanly close the connection (if any)."""
        if self.receiver is not None:
            self.receiver.stop()
            self.receiver.join()
            self.receiver = None

        if self.sock is not None:
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None

        print("[CLIENT] Disconnected.")

    # ------------------------------------------------------------------
    # Sending helpers
    # ------------------------------------------------------------------

    def _ensure_connected(self) -> bool:
        if self.sock is None:
            print("[CLIENT] Not connected. Use /connect <host> [port].")
            return False
        return True

    def _send_command(self, command: str, **kwargs) -> None:
        if not self._ensure_connected():
            return
        msg = make_command(command, **kwargs)
        try:
            self.sock.sendall(msg)
        except OSError as e:
            print(f"[CLIENT] Error sending command: {e}")
            self.disconnect()

    # ------------------------------------------------------------------
    # REPL
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
        print("Anything else is sent as a message to the current channel(s).\n")

        while self.running:
            try:
                user_input = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n[CLIENT] Exiting...")
                if self.sock is not None:
                    self._send_command("quit")
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                self._handle_command(user_input)
            else:
                self._send_command("message", text=user_input)

        if self.sock is not None:
            self.disconnect()

    def _handle_command(self, line: str) -> None:
        parts = line.split()
        cmd = parts[0][1:].lower()  # strip leading '/'

        if cmd == "connect":
            if len(parts) < 2:
                print("Usage: /connect <host> [port]")
                return
            host = parts[1]
            port = int(parts[2]) if len(parts) >= 3 else DEFAULT_PORT
            self.connect(host, port)

        elif cmd == "nick":
            if len(parts) < 2:
                print("Usage: /nick <name>")
                return
            self._send_command("nick", nickname=parts[1])

        elif cmd == "join":
            if len(parts) < 2:
                print("Usage: /join <channel>")
                return
            self._send_command("join", channel=parts[1])

        elif cmd == "leave":
            if len(parts) >= 2:
                self._send_command("leave", channel=parts[1])
            else:
                self._send_command("leave")

        elif cmd == "list":
            self._send_command("list")

        elif cmd == "quit":
            self._send_command("quit")
            self.running = False

        elif cmd == "help":
            print("Commands:")
            print("  /connect <host> [port]")
            print("  /nick <name>")
            print("  /join <channel>")
            print("  /leave [channel]")
            print("  /list")
            print("  /quit")
        else:
            print(f"[CLIENT] Unknown command: {cmd}. Try /help.")


def main() -> None:
    client = ChatClient()
    client.repl()


if __name__ == "__main__":
    main()
