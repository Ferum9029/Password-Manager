from Crypto.Cipher import ChaCha20
from base64 import b64decode
from typing import Dict, Tuple


class Cryptor:
    def __init__(self, key, nonce):
        self.data = tuple((key, nonce))

    @classmethod
    def load_from_encrypted_data(cls, data: Dict[str, str]):
        key = b64decode(data['key'].encode('utf-8'))
        nonce = b64decode(data['nonce'].encode('utf-8'))
        return cls(key=key, nonce=nonce)

    def decrypt(self, ciphered: bytes) -> bytes:
        return decrypt(self.data, ciphered)

    def encrypt(self, text: bytes) -> bytes:
        return encrypt(self.data, text)


def decrypt(data: Tuple[bytes, bytes], ciphered: bytes) -> bytes:
    cipher = ChaCha20.new(key=data[0], nonce=data[1])
    return cipher.decrypt(ciphered)


def encrypt(data: Tuple[bytes, bytes], text: bytes) -> bytes:
    cipher = ChaCha20.new(key=data[0], nonce=data[1])
    return cipher.encrypt(text)
