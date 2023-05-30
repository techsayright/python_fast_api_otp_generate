from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

def Hash(password):
    return pwd_context.hash(password)

def verify_Pass(password, hashed_password):
    return pwd_context.verify(password, hashed_password)