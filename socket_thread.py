# Standard libraries
import threading
import socket

# Imported libraries

# My libraries


class SocketThread(threading.Thread):
    """A class for socket thread"""
    def __init__(self, ispindel_tab_gui):
        super().__init__(daemon=True)
        self.ispindel_tab_gui = ispindel_tab_gui

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
            socket_message = ''

            try:
                while True:
                    self.socket_data = connection.recv(200).decode('utf-8')

                    # Extract socket message and pass it to 'iSpindel' tab
                    if self.socket_data:
                        socket_message += self.socket_data
                    else:
                        socket_message = eval(socket_message)
                        socket_message = {k.lower(): v for k, v in socket_message.items()}
                        self.ispindel_tab_gui.update_parameters(socket_message)
                        break
            finally:
                connection.close()
