import socket
import threading
import sys
import time

MAX_SIZE_DATAGRMM = 2048

class UDPclient:
    def __init__(self, host:str = '127.0.0.1', port:int = ...):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def setup(self):
        try:    self.sock.bind((self.host, self.port))
        except OSError:
            print("Port is busy. Try to change it.")
            return 0

        self.sock.connect(self.server_addr)

        self.sock.settimeout(30)

        return 1

    def send_inputmsg(self):
        while True:
            msg = input('')
            self.sock.send(msg.encode('utf-8'))

    def return_connection(self):
        msg = None
        while True:
            print('[CONNECTIONERROR]Trying to connect with server...')
            try:    msg = self.sock.recv(MAX_SIZE_DATAGRMM).decode()
            except ConnectionResetError:
                pass
            except socket.timeout:
                self.sock.send('#conn'.encode('utf-8'))
            else:
                return msg

    def handle(self):
        print('Write #join to connect with server...')
        threading.Thread(target=self.send_inputmsg, daemon=True).start()

        while True:
            msg = None
            try:    msg = self.sock.recv(MAX_SIZE_DATAGRMM).decode()
            except ConnectionResetError:
                print(self.return_connection())

            except socket.timeout:
                self.sock.send('#conn'.encode('utf-8'))
            if not msg:
                continue
            if msg != '[SERVER]Connected':
                print(msg)


if __name__ == '__main__':
    port = int(input('Your port: '))
    server_addr = tuple(input('Server("ip, port"): ').replace(' ', '').split(','))
    client = UDPclient(port = port)
    setattr(client, 'server_addr', ('127.0.0.1', 25))
    if client.setup():
        print(client.handle())
