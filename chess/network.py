import socket
import pickle
from registeration.constant import *
import ssl

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE


class Network:
    def __init__(self):
        self.server = SERVER
        self.port = PORT_NUM
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (self.server, self.port)
        self.player = self.connect()


    def connect(self):
        try:
            self.s.connect(self.addr)
            self.s = context.wrap_socket(self.s, server_hostname=SERVER)
            self.s.send(pickle.dumps("chess"))
            return pickle.loads(self.s.recv(4096*2))
        except:
            pass


    def send(self, data):
        try:
            self.s.send(pickle.dumps(data))
            return pickle.loads(self.s.recv(4096*2))
        except socket.error as e:
            print(e)

    def get_player(self):
        return self.player