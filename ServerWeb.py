import socket
from threading import Thread
from utils.ResponseBuilder import response_builder

#******************************CLASSE DE THREAD COM CLIENTE
class Client(Thread): #cada instância dessa classe possui um processo em execução para um único cliente
    #herança da classe Thread
    def __init__(self,socket_client,ip_Adress):   #método construtor da classe
        Thread.__init__(self)
        self.lista = ["GET", "HEAD"]
        self.socket_client = socket_client
        self.ip_Adress = ip_Adress 

    def run(self):#método é executado ao fazermos Thread.start()
        self.socket_client.setblocking(True)
        while True:
            try: #caso o socket esteja aberto
                msg = self.socket_client.recv(2000)  
            except:
                break
            data = msg.decode().split(" ")
            resposta , arq = self.response(data) #recebe corpo response e arquivo requisitado
            self.socket_client.sendall(resposta.encode())
            if(arq!=None):
                self.socket_client.sendall(arq)       
            self.socket_client.close()
            
    def response(self,dado):
        if(dado[0] in self.lista): #se a string estiver no array
            if(dado[0]=="GET"):
                return self.get(dado[1:]) #lista a partir do índice 1 em diante
            elif(dado[0]=="HEAD"):
                return self.head(dado[1:],False) #False: nnao quero receber o arquivo

        return (response_builder('HTTP', '1.1', '405', 'Method Not Allowed'), None)

    def get(self, dado):
        response, readFile = self.head(dado, True) #recebe cabeçalho do response e arquivo requisitado.
                                                    #True: quero receber arquivo se ele existir
        if(readFile!=None): #verifica se path contém / no início (fatiamento de string)
            diretorio = str.rpartition(dado[0], ".")#cria lista com diretório do arquivo e extensão
            print("[Arquivo solicitado:", dado[0], "]")
            if(diretorio[2].find("html")==-1):
                return (response, readFile) #envio de response e arquivo solicitado     
            else:
                response = response + readFile.decode("utf-8") 
                return (response, None) #página enviada no corpo response
        
        return (response_builder('HTTP', '1.1', '404', 'File not found'), None)


    def head(self, dado, flag):
        #método retorna cabeçalho de requisição e arquivo solicitado
        directory = str.rpartition(dado[0], ".")#cria lista com diretório do arquivo e extensão
        if(dado[0][0]=="/"): #verifica se path contém / no início (fatiamento de string)
            if(len(dado[0])==1):#retornar index.html da raiz do servidor
                try:
                    read_file = open('index.html', 'rb').read() #leitura como texto
                except:
                    return (response_builder('HTTP', '1.1', '404', 'File not found'), None)
            else: 
                try:#leitura de um arquivo qualquer
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
        
