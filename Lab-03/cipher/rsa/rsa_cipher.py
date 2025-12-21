import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


class RSACipher:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        self.keys_dir = os.path.join(base_dir, "keys")
        os.makedirs(self.keys_dir, exist_ok=True)
        self.private_key_path = os.path.join(self.keys_dir, "private_key.pem")
        self.public_key_path = os.path.join(self.keys_dir, "public_key.pem")

    def generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        with open(self.private_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

        with open(self.public_key_path, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    def load_keys(self):
        with open(self.private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend(),
            )

        with open(self.public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend(),
            )

        return private_key, public_key

    def encrypt(self, message: str, key):
        data = message.encode("utf-8")
        ciphertext = key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return ciphertext

    def decrypt(self, ciphertext: bytes, key):
        plaintext = key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plaintext.decode("utf-8")

    def sign(self, message: str, private_key):
        data = message.encode("utf-8")
        signature = private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return signature

    def verify(self, message: str, signature: bytes, public_key):
        data = message.encode("utf-8")
        try:
            public_key.verify(
                signature,
                data,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False