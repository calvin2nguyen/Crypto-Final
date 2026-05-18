import socket

from src.crypto.key_manager import (
    load_private_key,
    load_public_key
)

from src.crypto.encrypt import encrypt_message
from src.crypto.decrypt import decrypt_message

from src.crypto.signatures import sign_message


HOST = "127.0.0.1"
PORT = 5000

ATM_ID = "ATM1"


bank_public_key = load_public_key(
    "keys/bank_public.pem"
)


atm_rsa_private_key = load_private_key(
    "keys/atm1_private.pem"
)


print("Choose signature algorithm")
print("1. RSA")
print("2. DSA")

choice = input("> ")

if choice == "2":

    SIGNATURE_ALGORITHM = "DSA"

    signing_private_key = load_private_key(
        "keys/atm1_dsa_private.pem"
    )

else:

    SIGNATURE_ALGORITHM = "RSA"

    signing_private_key = load_private_key(
        "keys/atm1_private.pem"
    )


def send_secure_message(client_socket, message):

    encrypted_message = encrypt_message(
        bank_public_key,
        message
    )

    signature = sign_message(
        signing_private_key,
        message,
        SIGNATURE_ALGORITHM
    )

    signature = signature.ljust(256, b"\0")

    client_socket.sendall(
        SIGNATURE_ALGORITHM.encode().ljust(16)
    )

    client_socket.sendall(encrypted_message)

    client_socket.sendall(signature)


def receive_secure_message(client_socket):

    encrypted_data = client_socket.recv(256)

    return decrypt_message(
        atm_rsa_private_key,
        encrypted_data
    )


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

print("Connected to bank server")

send_secure_message(
    client,
    ATM_ID
)

print(
    receive_secure_message(client)
)


user_id = input("User ID: ")

password = input("Password: ")

send_secure_message(
    client,
    user_id
)

send_secure_message(
    client,
    password
)

print(
    receive_secure_message(client)
)


while True:

    print("\n1. Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Quit")

    choice = input("> ")

    if choice == "1":

        send_secure_message(
            client,
            "BALANCE"
        )

    elif choice == "2":

        amount = input("Amount: ")

        send_secure_message(
            client,
            f"DEPOSIT:{amount}"
        )

    elif choice == "3":

        amount = input("Amount: ")

        send_secure_message(
            client,
            f"WITHDRAW:{amount}"
        )

    elif choice == "4":
        
        send_secure_message(
            client,
            "QUIT"
        )

        print(
            receive_secure_message(client)
        )

        break

    else:
        print("Invalid option")
        continue

    print(
        receive_secure_message(client)
    )

client.close()