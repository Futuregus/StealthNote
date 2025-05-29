import os
import base64
from struct import pack, unpack
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import zlib

# Constants
SALT_SIZE = 64
backend = default_backend()
MAGIC_HEADER = b"ECTFv2.0::"
VERSION_BYTE = b"\x02"

# %--- Encryption Helper Class ---%
class EncryptionHelper:
    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=500000,
            backend=backend
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def encrypt_data(password: str, data: str) -> bytes:
        salt = os.urandom(SALT_SIZE)
        key = EncryptionHelper.derive_key(password, salt)
        compressed = zlib.compress(data.encode())
        encrypted = Fernet(key).encrypt(compressed)
        return MAGIC_HEADER + salt + encrypted

    @staticmethod
    def decrypt_data(password: str, encrypted_data: bytes) -> str:
        if not encrypted_data.startswith(MAGIC_HEADER):
            raise ValueError("Invalid file format. Not a valid .ectf file.")
        encrypted_data = encrypted_data[len(MAGIC_HEADER):]
        salt = encrypted_data[:SALT_SIZE]
        encrypted = encrypted_data[SALT_SIZE:]
        key = EncryptionHelper.derive_key(password, salt)
        decrypted_compressed = Fernet(key).decrypt(encrypted)
        decompressed = zlib.decompress(decrypted_compressed)
        return decompressed.decode()
# %----------------------%


# %--- File Manager Class ---%
class FileManager:
    @staticmethod
    def open_ectf(path, password):
        try:
            with open(path, "rb") as f:
                encrypted_data = f.read()
            return EncryptionHelper.decrypt_data(password, encrypted_data)
        except Exception as e:
            raise ValueError(f"Failed to open or decrypt file: {e}")

    @staticmethod
    def save_ectf(path, password, data):
        try:
            encrypted_data = EncryptionHelper.encrypt_data(password, data)
            with open(path, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            raise ValueError(f"Failed to encrypt or save file: {e}")
# %----------------------%
