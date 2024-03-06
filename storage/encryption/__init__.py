from storage.encryption import simple_cipher
from storage.encryption.encryptor import Cryptor
from os import getlogin, path, getcwd, remove
from Crypto.Random import get_random_bytes
from base64 import b64decode, b64encode
from typing import Tuple
from storage.encryption.exceptions import KeyFileNotFound
import json

username = getlogin()
working_dir = getcwd()
# k_data - key data. there are the key and the nonce
k_data_dir = f'{working_dir}\\storage\\k_data.kdt'


def k_data_exist():
    return path.exists(k_data_dir)


def create_k_data_file() -> None:
    key = b64encode(get_random_bytes(32)).decode('utf-8')
    nonce = b64encode(get_random_bytes(24)).decode('utf-8')
    data_in_json = json.dumps({'key': key, 'nonce': nonce})
    # using the simple cipher on it for more fun
    completed_json = SimpleCipher.encode(data_in_json)
    with open(k_data_dir, 'w') as f:
        f.write(completed_json)


def get_k_data_from_disk() -> Tuple[bytes, bytes]:
    if not path.exists(k_data_dir):
        raise KeyFileNotFound("There's no key file")
    with open(k_data_dir, 'r') as f:
        k_json = json.loads(SimpleCipher.decode(f.read()))
    key = b64decode(k_json['key'].encode('utf-8'))
    nonce = b64decode(k_json['nonce'].encode('utf-8'))
    return key, nonce


def delete_k_data_file() -> None:
    if not path.exists(k_data_dir):
        raise KeyFileNotFound("There's no key file")
    remove(k_data_dir)


class SimpleCipher:
    @staticmethod
    def encode(text: str) -> str:
        return simple_cipher.encrypt(text)

    @staticmethod
    def decode(text: str) -> str:
        return simple_cipher.decrypt(text)


class EncInterface:
    def __init__(self, key, nonce):
        self.encryptor = Cryptor(key, nonce)

    def decrypt(self, text: bytes) -> str:
        return self.encryptor.decrypt(text).decode('utf-8')

    def encrypt(self, text: str) -> bytes:
        return self.encryptor.encrypt(text.encode('utf-8'))
