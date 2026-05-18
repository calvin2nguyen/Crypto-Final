# scripts/generate_keys.py

import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa

from cryptography.hazmat.primitives import serialization


KEY_SIZE = 2048


def generate_rsa_key_pair(private_path, public_path):

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(private_path, "wb") as private_file:
        private_file.write(private_pem)

    with open(public_path, "wb") as public_file:
        public_file.write(public_pem)


def generate_dsa_key_pair(private_path, public_path):

    private_key = dsa.generate_private_key(
        key_size=KEY_SIZE
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(private_path, "wb") as private_file:
        private_file.write(private_pem)

    with open(public_path, "wb") as public_file:
        public_file.write(public_pem)


os.makedirs("keys", exist_ok=True)

# BANK RSA
generate_rsa_key_pair(
    "keys/bank_private.pem",
    "keys/bank_public.pem"
)

# ATM1 RSA
generate_rsa_key_pair(
    "keys/atm1_private.pem",
    "keys/atm1_public.pem"
)

# ATM2 RSA
generate_rsa_key_pair(
    "keys/atm2_private.pem",
    "keys/atm2_public.pem"
)

generate_dsa_key_pair(
    "keys/atm1_dsa_private.pem",
    "keys/atm1_dsa_public.pem"
)

generate_dsa_key_pair(
    "keys/atm2_dsa_private.pem",
    "keys/atm2_dsa_public.pem"
)

print("Keys generated successfully.")