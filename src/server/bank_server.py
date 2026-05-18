import socket
import threading
from src.server.client_handler import ClientHandler
from src.server.account_db import AccountDatabase

class BankServer:
                
        def __init__(self,host="127.0.0.1",port=5000):
            self.host = host
            self.port = port

            self.server_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
            self.account_db = AccountDatabase()
        def start(self):
            self.server_socket.bind((self.host,self.port))
            self.server_socket.listen()
            print(f"Server running on {self.host}:{self.port}")

            while True:
                client_socket, addr = self.server_socket.accept()
                handler = ClientHandler(client_socket=client_socket,
                                        address=addr,account_db=self.account_db)
                print(f"Connected to : {addr}")
                thread = threading.Thread(
                     target=handler.handle
                )
                thread.start()
        
if __name__ == "__main__":
    server = BankServer()
    server.start()
     
             
            

                
        