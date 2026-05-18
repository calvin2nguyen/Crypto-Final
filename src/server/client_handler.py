from src.server.auth import Authenticator
from src.crypto.signatures import verify_signature

from src.crypto.key_manager import ( load_private_key, load_public_key)
from src.crypto.encrypt import encrypt_message
from src.crypto.decrypt import decrypt_message


class ClientHandler:

    def __init__(self, client_socket, address, account_db):
        self.client_socket = client_socket
        self.address = address
        self.account_db = account_db

        self.auth = Authenticator()

        self.bank_private_key = load_private_key("keys/bank_private.pem")
        self.atm_encryption_key = None
        self.atm_signature_key = None
        self.atm_id = None
        self.user_id = None
        self.authenticated = False

    def handle(self):
        print(f"New connection from: {self.address}")

        try:
            self.authenticate_atm()
            self.authenticate_user()
            self.handle_requests()

        except Exception as e:
            print(f"{self.address}: {e}")

        finally:
            self.client_socket.close()
            print(f"Disconencted: {self.address}")

    def authenticate_atm(self):

        algorithm = (
            self.client_socket.recv(16)
            .decode()
            .strip()
        )

        encrypted_atm_id = self.client_socket.recv(256)
    
        signature = self.client_socket.recv(256)
        signature = signature.rstrip(b"\0")

        atm_id = decrypt_message(
            self.bank_private_key,
            encrypted_atm_id
        )

        if not self.auth.atm_valid(atm_id):
            raise Exception("Invalid ATM")

        self.atm_id = atm_id

        self.atm_encryption_key = load_public_key(
            f"keys/{atm_id.lower()}_public.pem"
        )

        if algorithm == "DSA":

            self.atm_signature_key = load_public_key(
                f"keys/{atm_id.lower()}_dsa_public.pem"
            )

        else:

            self.atm_signature_key = load_public_key(
                f"keys/{atm_id.lower()}_public.pem"
            )


        valid_signature = verify_signature(
            self.atm_signature_key,
            atm_id,
            signature,
            algorithm
        )

        if not valid_signature:
            raise Exception("Invalid ATM signature")

        self.send_secure_message(
            "ATM authenticated"
        )

        print(f"Authenticated Successfully: {atm_id}")

    def authenticate_user(self):
        user_id = self.receive_secure_message()
        password = self.receive_secure_message()

        if not self.auth.valid_user(user_id):
            self.send_secure_message("Invalid user ID")
            raise Exception("Invalid user ID")

        login_success = self.auth.verify_user(
            self.account_db,
            user_id,
            password
        )

        if login_success:
            self.user_id = user_id
            self.authenticated = True
            self.send_secure_message("Login successful")
            print(f"Login Successful: user {user_id}")
        else:
            self.send_secure_message("Login failed")
            raise Exception("user login failed")

    def handle_requests(self):
        while self.authenticated:
            request = self.receive_secure_message()

            if request == "BALANCE":
                self.handle_balance()

            elif request.startswith("DEPOSIT:"):
                self.handle_deposit(request)

            elif request.startswith("WITHDRAW:"):
                self.handle_withdraw(request)

            elif request == "ACTIVITY":
                self.handle_activity()

            elif request == "QUIT":
                self.send_secure_message("Goodbye")
                break

            else:
                self.send_secure_message("Invalid request")

    def handle_balance(self):
        balance = self.account_db.get_balance(self.user_id)
        self.send_secure_message(f"Balance: ${balance:.2f}")

    def handle_deposit(self, request):
        try:
            amount = float(request.split(":")[1])

            if amount <= 0:
                self.send_secure_message("Deposit amount must be positive")
                return

            self.account_db.deposit(self.user_id, amount)
            self.send_secure_message(f"Deposit successful: ${amount:.2f}")

        except ValueError:
            self.send_secure_message("Invalid deposit amount")

    def handle_withdraw(self, request):
        try:
            amount = float(request.split(":")[1])

            if amount <= 0:
                self.send_secure_message("Withdrawal amount must be positive")
                return

            success = self.account_db.withdraw(self.user_id, amount)

            if success:
                self.send_secure_message(f"Withdrawal successful: ${amount:.2f}")
            else:
                self.send_secure_message("Insufficient funds")

        except ValueError:
            self.send_secure_message("Invalid withdrawal amount")

    def handle_activity(self):
        activity = self.account_db.get_activity(self.user_id)

        if not activity:
            self.send_secure_message("No account activity")
        else:
            self.send_secure_message("\n".join(activity))

    def receive_secure_message(self):

        algorithm = (
            self.client_socket.recv(16)
            .decode()
            .strip()
        )

        encrypted_data = self.client_socket.recv(256)

        signature = self.client_socket.recv(256)
        signature = signature.rstrip(b"\0")

        if not encrypted_data:
            raise Exception("Client disconnected")

        message = decrypt_message(
            self.bank_private_key,
            encrypted_data
        )

        valid_signature = verify_signature(
            self.atm_signature_key,
            message,
            signature,
            algorithm
        )

        if not valid_signature:
            raise Exception("Invalid signature")

        return message

    def send_secure_message(self, message):

        encrypted_message = encrypt_message(
            self.atm_encryption_key,
            message
        )
        self.client_socket.send(encrypted_message)