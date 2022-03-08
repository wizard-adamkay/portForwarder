class Connection:
    def __init__(self, from_port, to_port, to_ip):
        self.from_port = int(from_port)
        self.to_port = int(to_port)
        self.to_ip = to_ip
