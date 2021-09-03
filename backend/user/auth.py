from datetime import datetime, timedelta
from typing import Optional
from fastapi import status, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
import jwt

SECRET_KEY = "7yiurhg9rgv98hvoidshvr8e9vyue90vj90eo"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data, expire_minutes: Optional[int] = None):
    if expire_minutes:
        expire = datetime.utcnow() + timedelta(expire_minutes)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encoded_jwt = jwt.encode({
        'sub': data,
        'exp': expire,
    }, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Signature has expired')
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

def get_current_user(auth: HTTPAuthorizationCredentials = Security(security)):
    return verify_token(auth.credentials)