from fastapi import FastAPI, HTTPException
from jsonrpcclient.requests import request_uuid
from authlib.integrations.starlette_client import OAuthError
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime

import httpx

from jwtoken import create_token
from jwtoken import valid_email_from_db
from jwtoken import create_refresh_token
from jwtoken import decode_token
from jwtoken import add_user_to_db
from jwtoken import CREDENTIALS_EXCEPTION
from oauth import oauth
from utils import endpoint_auth


auth_app = FastAPI()
auth_app.add_middleware(SessionMiddleware, secret_key="!secret")


@auth_app.route("/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8080/token"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_app.route("/token")
async def token(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise CREDENTIALS_EXCEPTION
    user_data = await oauth.google.parse_id_token(request, access_token)
    access_token = create_token(user_data["email"])
    refresh_token = create_refresh_token(user_data["email"])
    user_data["access_token"] = access_token
    user_data["refresh_token"] = refresh_token
    await add_user_to_db(user_data)
    return JSONResponse(
        {
            "result": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@auth_app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


@auth_app.post("/refresh")
async def refresh(request: Request):
    try:
        form = await request.json()
        if form.get("grant_type") == "refresh_token":
            token = form.get("refresh_token")
            payload = decode_token(token)
            # Check if token is not expired
            if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
                email = payload.get("sub")
                # Validate email
                if valid_email_from_db(email):
                    # Create and return token
                    return JSONResponse(
                        {"result": True, "access_token": create_token(email)}
                    )

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION


# DUMMY


@auth_app.get("/dummy/login")
async def dummy_login():
    return JSONResponse(
        {
            "result": "true",
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJscmF6b3ZpY0BnbWFpbC5jb20iLCJleHAiOjE2NDM0MDc5NDd9._h426jMZXWJ5zwclxtkg4A8xe7-GxJB-XgGa55EYfBQ",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJscmF6b3ZpY0BnbWFpbC5jb20iLCJleHAiOjE2NDU5OTkwNDd9.iZjQTbf004zjqTqxEkGWbDSncdmAyj3-K39uVuFfENs",
        }
    )


@auth_app.get("/dummy/token")
async def dummy_token():
    try:
        data = {
            "iss": "https://accounts.google.com",
            "azp": "32814020986-9u0gu68a62jh6o7i7drv5ltrpuf18emv.apps.googleusercontent.com",
            "aud": "32814020986-9u0gu68a62jh6o7i7drv5ltrpuf18emv.apps.googleusercontent.com",
            "sub": "100453178713727110711",
            "email": "lrazovic@gmail.com",
            "email_verified": "true",
            "at_hash": "ZAlXWOwZQ0a7NdC09HOn8g",
            "nonce": "H8CHfv8hV6RJy40F9r4P",
            "name": "Leonardo Razovic",
            "picture": "https://lh3.googleusercontent.com/a/AATXAJz6ZNHbViGfyqwaRiy-A3ikxAvc3njHFiPK9LQI=s96-c",
            "given_name": "Leonardo",
            "family_name": "Razovic",
            "locale": "en-GB",
            "iat": "1644142365",
            "exp": "1644145965",
        }
        data["access_token"] = create_token(data["email"])
        data["refresh_token"] = create_refresh_token(data["email"])
        await add_user_to_db(data)
        return JSONResponse(data)
    except Exception as e:
        print(e)
        return {"status": "error"}


@auth_app.get("/dummy/readdb")
async def dummy_readdb():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                endpoint_auth,
                json=request_uuid("read_db"),
            )
        if response.is_error:
            raise HTTPException(status_code=404, detail="Error in JSON-RPC response")
        else:
            return response.json()
    except:
        raise HTTPException(
            status_code=500, detail="Impossible to connect to JSON-RPC Server"
        )
