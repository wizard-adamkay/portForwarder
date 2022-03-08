import socket
import time

HOST = "localhost"  # The server's hostname or IP address
PORT = 8015  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(20):
        time.sleep(1)
        s.sendall(b"Hello, world")
        data = s.recv(1024)
        print(f"Received {data!r}")


