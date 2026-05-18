

class ClientHandler:
    def __init__(self,client_socket, address):
        self.client_socket = client_socket
        self.address = address
 
    def handle(self):
        print (f"Handling {self.address}")
        while True:
            data_received = self.client_socket.recv(1024)
            if not data_received:
                 break
            print(data_received.decode())
            message = "Message has been received".encode()
            self.client_socket.send(message)
        self.client_socket.close()
        print(f"Disconnected from {self.address}")