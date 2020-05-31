import json
import socket

from libs.logger_setup import get_logger
from modules.module_base import ModuleBase

logger = get_logger()

HOST_MAC = 'B8:27:EB:87:5B:87'
PORT = 3
BACKLOG = 1
SIZE = 1024

class RemoteControlModule(ModuleBase):
    def __init__(self, state):
        DEFAULT_CADENCE_S = 0.1
        super().__init__(state, cadence=DEFAULT_CADENCE_S)
        self.server = socket.socket(socket.AF_BLUETOOTH, 
                                   socket.SOCK_STREAM, 
                                   socket.BTPROTO_RFCOMM)
        self.server.setblocking(False)
        self.server.bind((HOST_MAC, PORT))
        self.server.listen(BACKLOG)
        self.troll_connected = False
        self.client = None
        print("Server ready")

    def handshake_troll(self):
        try:
            print("Server trying to connect")
            self.client, address = self.server.accept()
            print("server connected")
            self.client.setblocking(False)
            print("Server waiting for data")
            data = self.client.recv(SIZE)
            print("Server has recieved data")
            if "Hello Igor" in str(data):
                print(data)
                self.troll_connected = True
                self.client.send(bytes('Hello Troll', 'UTF-8'))
        except socket.error:
            if self.client:
                self.client.close()
            self.troll_connected = False

    def step(self):
        if not self.troll_connected:
            self.handshake_troll()
            
