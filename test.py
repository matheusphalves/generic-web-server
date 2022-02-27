from http import server
from Server import Server


server_instance = Server()

server_instance.start_server()
server_instance.close_server()