import socket
from datetime import datetime
from ServerWeb import Client


class Server:
    def __init__(self, port = 5001, address = '', max_connections = 5) -> None:
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
            raise f'Error during server initialization: {ex}' 

    def start_server(self):
        print(f'Starting server on: {self.address}:{self.port}')
        start_time = datetime.now()
        while self.__isAlive:
            connection, adress  = self.server_socket.accept() #retorna socket de conexão realizado e endereço do usuário
            new_process = Client(connection, adress) #creating new instance of Client class
            new_process.start() #start proccess with conection received
        end_time = datetime.now()
        print(f'Finished execution. Duration: {end_time - start_time}')

    def close_server(self):
        self.__isAlive = False
        print('Closing server...')
        self.server_socket.close()
        