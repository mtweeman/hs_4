# Standard libraries
import threading
import socket
from time import *
import datetime

# Imported libraries

# My libraries


class RequesterSocketThread(threading.Thread):
    """A class for socket requester thread"""
    def __init__(self, master_gui, master_parameters):
        threading.Thread.__init__(self, daemon=True)
        self.master_gui = master_gui
        self.master_parameters = master_parameters
        self.connection = None
        self.write = []
        self.start_time = 0

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (socket.gethostname(), 10002)
        self.sock.bind(server_address)

        # Listen for incoming connections (max before refusing)
        self.sock.listen(1)

        self.start()

    def run(self):
        difference = 5

        while True:
            while not self.connection:
                self.establish_connection()

            # Read
            if self.connection and (datetime.datetime.now() - self.start_time).total_seconds() > difference:
                print('read')
                self.send()
                self.start_time = datetime.datetime.now()

            # Write
            if self.connection and self.write:
                print('write')
                self.send(self.write[0])
                if self.connection:
                    del self.write[0]

            sleep(0.1)

    def transmit(self, msg):
        self.write.append(msg)

    def establish_connection(self):
        # Waiting for connection
        (self.connection, client_address) = self.sock.accept()

        # Providing status of microcontroller and sensors
        self.master_gui.slave_socket_parameters_update(eval('{"microcontroller": "online"}'))
        print('Connection with', self.connection)

        self.send('sensors')

        # Putting 'write' (=_set) parameters in write queue
        for k, v in self.master_parameters.items():
            if ('_set' in k and 'set_' not in k) or\
                    ('_offset' in k and 'offset_' not in k):
                self.transmit(k + '=' + str(v))

        self.start_time = datetime.datetime.now()

    def send(self, msg=None):
        socket_message_raw = ''

        try:
            if not msg:
                self.connection.send(bytes('read', 'utf-8'))
            else:
                self.connection.send(bytes(msg, 'utf-8'))

            while True:
                piece = self.connection.recv(1000).decode('utf-8')

                if piece == '0':
                    print(socket_message_raw)
                    if socket_message_raw:
                        self.master_gui.slave_socket_parameters_update(eval(socket_message_raw))
                    break
                else:
                    socket_message_raw += piece

        except ConnectionResetError:
            print('Connection with ' + str(self.connection.getpeername()) + ' lost.')
            self.connection = None
            self.master_gui.slave_socket_parameters_update(eval("{'microcontroller': 'offline', 'sensors': 'offline'}"))
        except TimeoutError:
            print('Timeout error with ' + str(self.connection.getpeername()) + '.')
            self.connection = None
            self.master_gui.slave_socket_parameters_update(eval("{'microcontroller': 'offline', 'sensors': 'offline'}"))
