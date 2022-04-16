import socket

MAX_SIZE_DATAGRMM = 2048

class UDPserver:
    def __init__(self, host: str = '127.0.0.1', port: int = 25):
        self.host= host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clients = []

    def setup(self):
        # try!
        self.sock.bind((self.host, self.port))

    def listen(self):
        while True:
            msg, addr = None,None
            try:    msg, addr = self.sock.recvfrom(MAX_SIZE_DATAGRMM)
            except ConnectionResetError:
                continue

            if not msg:
                continue

            #checking connection
            if msg.decode() == '#conn':
                self.sock.sendto('[SERVER]Connected'.encode('utf-8'), addr)
                continue

            #add new client
            if msg.decode() == '#join' and addr not in self.clients:
                self.clients += [addr]
                print('Current clients:', *self.clients)

                self.sock.sendto(f'[SERVER]Welcome to the chat!'.encode('utf-8'), addr)
                continue

            msg = f'{addr[0]}:{addr[1]}: {msg.decode()}'
            print(f'[LOGS] {msg}' if addr in self.clients else f'[LOGS] [This address isnt client of chat!] {msg}')
            for client in self.clients:
                if client != addr:
                    self.sock.sendto(msg.encode('utf-8'), client)


if __name__ == '__main__':
    server = UDPserver()
    server.setup()
    server.listen()
