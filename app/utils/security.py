from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password: str) -> str:
    if password.startswith("$2b$") or password.startswith("$2a$"):
        return password

    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verifyPassword(plain_password: str, hashed_password: str) -> bool:
    # evita senhas longas demais
    if len(plain_password) > 72:
        plain_password = plain_password[:72]

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print("Erro ao verificar senha:", e)
        return False

def createAcessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token

def decodeToken(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None