import socket
import pickle
from tic_tac_toe.constant import *



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
            self.s.send(pickle.dumps("tic tac toe"))
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