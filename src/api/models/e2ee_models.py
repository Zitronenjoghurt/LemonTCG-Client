from pydantic import BaseModel

class E2EEPublicKey(BaseModel):
    key: str

class E2EEEncryptedPrivateKey(BaseModel):
    key: str
    salt_hex: str