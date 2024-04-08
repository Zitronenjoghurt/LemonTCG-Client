import base64
import os
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordError(Exception):
    def __init__(self) -> None:
        super().__init__("The provided password is wrong.")

class E2EEInformation(BaseModel):
    public_key: str
    encrypted_private_key: str
    salt_hex: str

def generate_e2ee(password: str) -> E2EEInformation:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Generate random salt, making it harder to decrypt
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = kdf.derive(password.encode())

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(key)
    )

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    base64_public_key = base64.b64encode(pem_public_key).decode('utf-8')
    base64_encrypted_private_key = base64.b64encode(pem_private_key).decode('utf-8')

    return E2EEInformation(
        public_key=base64_public_key,
        encrypted_private_key=base64_encrypted_private_key,
        salt_hex=salt.hex()
    )

def load_public_key(base64_public_key: str):
    pem_public_key = base64.b64decode(base64_public_key.encode('utf-8'))
    return serialization.load_pem_public_key(pem_public_key)

def decrypt_private_key(base64_encrypted_private_key: str, salt_hex: str, password: str):
    encrypted_private_key = base64.b64decode(base64_encrypted_private_key.encode('utf-8'))
    salt = bytes.fromhex(salt_hex)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())

    private_key = serialization.load_pem_private_key(
        encrypted_private_key,
        password=key,
    )
    return private_key

def encrypt_data(public_key, data: str) -> str:
    encrypted_data: bytes = public_key.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_data(private_key, encrypted_data: str) -> str:
    encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
    decrypted_data = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode('utf-8')

def check_keys(public_key, private_key) -> bool:
    data = "Lorem ipsum dolores"
    encrypted_data = encrypt_data(public_key=public_key, data=data)
    decrypted_data = decrypt_data(private_key=private_key, encrypted_data=encrypted_data)
    return data == decrypted_data