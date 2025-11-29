import json

def make_command(command, **kwargs):
    """
    Build a JSON command object.
    """
    obj = {
        "type": "command",
        "command": command,
        "args": kwargs
    }
    return json.dumps(obj).encode()

def make_event(event, **kwargs):
    """
    Build a JSON event object from server to client.
    """
    obj = {
        "type": "event",
        "event": event,
        "args": kwargs
    }
    return json.dumps(obj).encode()

def parse_message(data):
    """
    Convert bytes → Python dict
    """
    try:
        return json.loads(data.decode())
    except Exception:
        return None