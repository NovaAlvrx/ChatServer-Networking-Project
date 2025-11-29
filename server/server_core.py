class ServerCore:
    def __init__(self):
        self.nicknames = {}          # socket → nickname
        self.channels = {}           # channel → set of sockets

    def set_nick(self, conn, nickname):
        self.nicknames[conn] = nickname

    def get_nick(self, conn):
        return self.nicknames.get(conn, "Unknown")

    def ensure_channel(self, channel):
        if channel not in self.channels:
            self.channels[channel] = set()

    def join_channel(self, conn, channel):
        self.ensure_channel(channel)
        self.channels[channel].add(conn)

    def leave_channel(self, conn, channel):
        if channel in self.channels and conn in self.channels[channel]:
            self.channels[channel].remove(conn)

    def list_channels(self):
        return {ch: len(users) for ch, users in self.channels.items()}

    def get_user_channels(self, conn):
        return [ch for ch, users in self.channels.items() if conn in users]

    def broadcast(self, channel, message_bytes):
        if channel not in self.channels:
            return
        for user_conn in self.channels[channel]:
            try:
                user_conn.sendall(message_bytes)
            except:
                pass  # ignore broken connections