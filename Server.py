import socket
from datetime import datetime
from ServerWeb import Client


class Server:
    """A class that represents a Server listening your Clients.
        Attributes
    ----------
    port : int
        represents the port used to bind. The default value is 5001
    address : str
        represents the address used to make requests. The default value is http://localhost

    max_connections : int
        represents the number of the max simultaneous connections on server
    """

    def __init__(self, port = 5001, address = 'localhost', max_connections = 5) -> None:
        self.port = port
        self.max_connections = max_connections
        self.address = address
        self.create_socket()
        self.__isAlive = True

    def create_socket(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.address, self.port))
            self.server_socket.listen(self.max_connections)

        except Exception as ex:
            print(f'Error during server initialization: {ex}') 

    def start_server(self):
        print(f'Starting server on: {self.address}:{self.port}')
        start_time = datetime.now()
        while self.__isAlive:
            connection, address  = self.server_socket.accept() #return socket and user address
            print(address)
            print(connection)
            new_process = Client(connection, address) #creating new instance of Client class
            new_process.start() #start proccess with conection received
        end_time = datetime.now()
        print(f'Finished execution. Duration: {end_time - start_time}')

    def close_server(self):
        self.__isAlive = False
        print('Closing server...')
        self.server_socket.close()
        