import socket
import json
import time
from threading import Thread
from connection import Connection


def get_ports_to_forward():
    read_file = open('config.json')
    data = json.load(read_file)
    connections = []
    for conn in data["connections"]:
        connections.append(Connection(conn["from_port"], conn["to_port"], conn["to_ip"]))
    return connections


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return "localhost"


def make_connections(arr):
    for conn in arr:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((get_my_ip(), conn.from_port))
        print("listening on port: " + str(conn.from_port))
        s.listen(5)
        Thread(target=connection_handler, args=(s, conn,)).start()


def transfer_packets(inbound_socket, outbound_socket):
    try:
        while True:
            data = inbound_socket.recv(1024)
            outbound_socket.sendall(data)
            if not data:
                print("no data to read! closing connections...")
                break

    except Exception as e:
        print("")
    finally:
        inbound_socket.close()


def connection_handler(s, conn):
    try:
        while True:
            c, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1])
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((conn.to_ip, conn.to_port))
            Thread(target=transfer_packets, args=(c, sock,)).start()
            Thread(target=transfer_packets, args=(sock, c,)).start()

    except Exception as e:
        print(e)


if __name__ == '__main__':
    connections = get_ports_to_forward()
    make_connections(connections)
    while True:
        time.sleep(1)
