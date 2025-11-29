# protocol.py
import json
import socket
from typing import Optional


ENCODING = "utf-8"


def send_obj(sock: socket.socket, obj: dict) -> None:
    """
    Send a JSON object over a socket, terminated with a newline.
    """
    data = json.dumps(obj) + "\n"
    sock.sendall(data.encode(ENCODING))


def recv_obj_from_file(f):
    """
    Read one JSON object from a file-like object (e.g. sock.makefile()).
    Returns:
      - dict on success
      - None if connection is closed
    """
    line = f.readline()
    if not line:
        return None
    return json.loads(line)


# --- Convenience constructors for our commands -------------------------


def cmd_nick(nick: str) -> dict:
    return {"type": "command", "action": "nick", "nickname": nick}


def cmd_list() -> dict:
    return {"type": "command", "action": "list"}


def cmd_join(channel: str) -> dict:
    return {"type": "command", "action": "join", "channel": channel}


def cmd_leave(channel: Optional[str] = None) -> dict:
    # channel can be None; server can use "current" channel in that case
    return {"type": "command", "action": "leave", "channel": channel}


def cmd_quit() -> dict:
    return {"type": "command", "action": "quit"}


def cmd_message(channel: str, text: str) -> dict:
    return {
        "type": "command",
        "action": "message",
        "channel": channel,
        "text": text,
    }
