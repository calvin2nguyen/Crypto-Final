from cryptography.hazmat.primitives import serialization


def load_private_key(file_path):
    with open(file_path, "rb") as key_file:

        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    return private_key


def load_public_key(file_path):
    with open(file_path, "rb") as key_file:

        public_key = serialization.load_pem_public_key(
            key_file.read()
        )

    return public_key