from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(password: str, hash_password: str) -> bool:
    return CRIPTO.verify(password, hash_password)

def generate_password_hash(password: str) -> str:
    return CRIPTO.hash(password)