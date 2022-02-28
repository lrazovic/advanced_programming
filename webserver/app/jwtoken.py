import os
from datetime import datetime
from datetime import timedelta

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jsonrpcclient.requests import request_uuid
from utils import cast_to_number, endpoint_persistence
import httpx


load_dotenv()


# Configuration
API_SECRET_KEY = os.environ.get("GOOGLE_CLIENT_SECRET") or None
if API_SECRET_KEY is None:
    raise BaseException("Missing API_SECRET_KEY env var.")
API_ALGORITHM = os.environ.get("API_ALGORITHM") or "HS256"
API_ACCESS_TOKEN_EXPIRE_MINUTES = (
    cast_to_number("API_ACCESS_TOKEN_EXPIRE_MINUTES") or 60 * 24 * 3
)
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# Token url (We should later create a token url that accepts just a user and a password to use it with Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


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


def create_refresh_token(email):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": email}, expires_delta=expires)


# Create token for an email
def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return access_token


def valid_email_from_db(email):
    try:
        with httpx.Client() as client:
            response = client.post(
                endpoint_persistence,
                json=request_uuid("valid_email_from_db", params=[email]),
            )
        if response.is_error:
            return False
        else:
            if response.json()["result"] == True:
                return True
            else:
                return False
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


async def add_user_to_db(user_data):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("add_user_to_db", params=[user_data]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


def decode_token(token):
    return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])


def get_current_user_email(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    if valid_email_from_db(email):
        return email

    raise CREDENTIALS_EXCEPTION


async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    _ = get_current_user_email(token)
    return token


#################################################
async def check_user_db(email, password):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("valid_user_from_db", params=[email, password]),
            )
        if response.is_error:
            return {"error": response.json}
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


async def get_user_data(email):
    try:
        async with httpx.AsyncClient() as client:
            print(endpoint_persistence)
            response = await client.post(
                endpoint_persistence,
                json=request_uuid("getLoggedUser", params=[email]),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )


async def change_password(email, oldPass, newpassword):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_persistence,
                json=request_uuid(
                    "update_user_pass", params=[email, oldPass, newpassword]
                ),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )
