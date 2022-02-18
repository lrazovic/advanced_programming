from fastapi import FastAPI
from authlib.integrations.starlette_client import OAuthError
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime

from jwtoken import (
    create_token,
    valid_email_from_db,
    create_refresh_token,
    decode_token,
    add_user_to_db,
    CREDENTIALS_EXCEPTION,
)
from oauth import oauth
from utils import redirect_uri


auth_app = FastAPI()
auth_app.add_middleware(SessionMiddleware, secret_key="!secret")


@auth_app.route("/login")
async def login(request: Request):
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
    response = await add_user_to_db(user_data)
    return JSONResponse(
        {
            "result": True,
            "user_id": response["result"],
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
