import os
from datetime import datetime
from datetime import timedelta

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv


# Create a fake db:
FAKE_DB = {"lrazovic@gmail.com": {"name": "Leonardo Razovic"}}
load_dotenv()

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


# Configuration
API_SECRET_KEY = os.environ.get("GOOGLE_CLIENT_SECRET") or None
if API_SECRET_KEY is None:
    raise BaseException("Missing API_SECRET_KEY env var.")
API_ALGORITHM = os.environ.get("API_ALGORITHM") or "HS256"
API_ACCESS_TOKEN_EXPIRE_MINUTES = (
    cast_to_number("API_ACCESS_TOKEN_EXPIRE_MINUTES") or 15
)

# Token url (We should later create a token url that accepts just a user and a password to use it with Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30


def create_refresh_token(email):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": email}, expires_delta=expires)


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


# Create token for an email
def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return access_token


def valid_email_from_db(email):
    return email in FAKE_DB


def add_email_to_db(user_data):
    FAKE_DB[user_data["email"]] = user_data["name"]


def decode_token(token):
    return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])


async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    try:
        payload = payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    if valid_email_from_db(email):
        return email

    raise CREDENTIALS_EXCEPTION
