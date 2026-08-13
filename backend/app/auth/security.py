import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext

SECRET_KEY = "SUPER_SECRET_KEY_FOR_AUTONOMOUS_TESTING_ENGINEER_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # Fallback to PBKDF2 sha256 via hashlib
        if hashed_password.startswith("pbkdf2_fallback$"):
            _, salt, h_val = hashed_password.split("$")
            calc = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
            return calc == h_val
        return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception:
        # Standard library PBKDF2 fallback requiring zero third-party C dependencies
        salt = os.urandom(16).hex()
        h_val = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
        return f"pbkdf2_fallback${salt}${h_val}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
