from threading import Thread
from utils.ResponseBuilder import response_builder

class Client(Thread):
    """A class that represents a Client conection, inheriting a thread of control.
    To execute this class, was necessary to overring the run() method.
    """

    def __init__(self,socket_client,ip_Adress):
        Thread.__init__(self)
        self.lista = ["GET", "HEAD"]
        self.socket_client = socket_client
        self.ip_Adress = ip_Adress 

    def run(self):#called when type Thread.start()
        self.socket_client.setblocking(True)
        while True:
            try:
                msg = self.socket_client.recv(2000)  
            except:
                break
            data = msg.decode().split(" ")
            print(data[0])
            resposta , arq = self.response(data) #retrives response body and resource
            self.socket_client.sendall(resposta.encode())
            if(arq!=None):
                self.socket_client.sendall(arq)       
            self.socket_client.close()
            
    def response(self,dado):
        if(dado[0] in self.lista): #it's a allowed method
            if(dado[0]=="GET"):
                return self.get(dado[1:]) #handle GET
            elif(dado[0]=="HEAD"):
                return self.head(dado[1:],False) #handle HEAD

        return (response_builder('HTTP', '1.1', '405', 'Method Not Allowed'), None)

    def get(self, dado):
        response, readFile = self.head(dado, True) #retrives request headers and requested resource
                                                    #True: that's means the server needs return the requested file
        
        if(readFile!=None): #check if path contains '/' on start
            diretorio = str.rpartition(dado[0], ".")#create list with path to file
            print("[Arquivo solicitado:", dado[0], "]")
            if(diretorio[2].find("html")==-1):
                return (response, readFile) #send response and requested file     
            else:
                response = response + readFile.decode("utf-8") 
                return (response, None) #send page in response body
        
        return (response_builder('HTTP', '1.1', '404', 'File not found'), None)


    
    def head(self, dado, flag):
        #returns headers and resource of request call
        directory = str.rpartition(dado[0], ".") #create list with path to file
        if(dado[0][0]=="/"): #check if path contains '/' on start
            if(len(dado[0])==1):#returns index.html from root path
                try:
                    read_file = open('index.html', 'rb').read()
                except:
                    return (response_builder('HTTP', '1.1', '404', 'File not found'), None)
            else: 
                try:
                    directory = str.rpartition(dado[0], ".")
                    read_file = open(directory[0][1:] + "." + directory[2], 'rb').read()
                except:
                    return (response_builder('HTTP', '1.1', '404', 'File not found'), None)

            if(read_file!=None):
                response = "HTTP/1.1 200 OK\r\n" + "Connection: close\r\n" + \
                    "Content Lenght:" + str(len(read_file)) + "\r\nContent Type:" + \
                        directory[1] + directory[2] + "\r\n\r\n"
                if flag:
                    return (response, read_file) #returning response and read file
                else:
                    return (response, None) #returning only response content
                
        return (response_builder('HTTP', '1.1', '404', 'File not found'), None)
        
