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

    def handshake_troll(self):
        try:
            self.client, address = self.server.accept()
            self.client.setblocking(False)
            data = self.client.recv(SIZE)
            if data:
                print(data)
                self.troll_connected = True
        except socket.error:
            if self.client:
                self.client.close()
            self.troll_connected = False

    def step(self):
        if not self.troll_connected:
            self.handshake_troll()
            
