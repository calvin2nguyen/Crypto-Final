import socket
import threading

class BankServer:
                
        def __init__(self,host="127.0.0.1",port=5000):
            self.host = host
            self.port = port

            self.server_socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )
        def start(self):
            self.server_socket.bind((self.host,self.port))
            self.server_socket.listen()
            print(f"Server running on {self.host}:{self.port}")

            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Connected to : {addr}")
                thread = threading.Thread(
                     target=self.handle_client,
                     args=(client_socket,)
                )
                thread.start()
        def handle_client(self,client_socket):
            while True:
                data_received = client_socket.recv(1024)
                if not data_received:
                     break
                print(data_received.decode())
                message = "Message has been received".encode()
                client_socket.send(message)
            client_socket.close()
        
if __name__ == "__main__":
    server = BankServer()
    server.start()
     
             
            

                
        