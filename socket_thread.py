# Standard libraries
import threading
import socket
import datetime
from collections import OrderedDict

# Imported libraries

# My libraries


class SocketThread(threading.Thread):
    """A class for socket thread"""
    def __init__(self, ispindel_tab_gui, fermentation_tab_gui):
        super().__init__(daemon=True)
        self.ispindel_tab_gui = ispindel_tab_gui
        self.fermentation_tab_gui = fermentation_tab_gui

        self.socket_message = OrderedDict.fromkeys(['measurement_time',
                                                    'name',
                                                    'angle',
                                                    'temperature',
                                                    'temp_units',
                                                    'battery',
                                                    'gravity',
                                                    'interval',
                                                    'rssi'],
                                                   )

        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (socket.gethostname(), 9501)
        self.sock.bind(server_address)

        # Listen for incoming connections (max before refusing)
        self.sock.listen(5)

        self.start()
        self.socket_data = {}

    def run(self):
        while True:
            # Wait for a connection
            (connection, client_address) = self.sock.accept()
            socket_message_raw = ''

            try:
                while True:
                    self.socket_data = connection.recv(200).decode('utf-8')

                    # Extract socket message and pass it to 'iSpindel' tab
                    if self.socket_data:
                        socket_message_raw += self.socket_data
                    else:
                        socket_message = eval(socket_message_raw)
                        socket_message = {k.lower(): v for k, v in socket_message.items()}

                        # Remove unnecessary keys
                        for key in self.socket_message:
                            if key != 'measurement_time' and key != 'gravity':
                                self.socket_message[key] = socket_message[key]

                        # Add measurement date and time
                        self.socket_message['measurement_time'] = datetime.datetime.now()

                        self.ispindel_tab_gui.update_parameters(self.socket_message)

                        socket_message_copy = self.socket_message.copy()
                        del (socket_message_copy['temp_units'],
                             socket_message_copy['interval'],
                             )

                        self.fermentation_tab_gui.update_parameters(socket_message_copy)
                        break
            finally:
                connection.close()
