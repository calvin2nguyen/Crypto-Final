# crypto/signatures.py

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def sign_message(private_key, message, algorithm):

    if isinstance(message, str):
        message = message.encode()

    algorithm = algorithm.upper()

    if algorithm == "RSA":
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return signature

    elif algorithm == "DSA":
        signature = private_key.sign(
            message,
            hashes.SHA256()
        )

        return signature

    else:
        raise ValueError("Unsupported signature algorithm")


def verify_signature(public_key, message, signature, algorithm):

    if isinstance(message, str):
        message = message.encode()

    algorithm = algorithm.upper()

    try:
        if algorithm == "RSA":
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

        elif algorithm == "DSA":
            public_key.verify(
                signature,
                message,
                hashes.SHA256()
            )

        else:
            raise ValueError("Unsupported signature algorithm")

        return True

    except InvalidSignature:
        return False