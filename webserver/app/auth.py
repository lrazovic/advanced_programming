from fastapi import FastAPI
from authlib.integrations.starlette_client import OAuthError
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from models import User, Login_form, Pass_change_form
from jwtoken import (
    create_token,
    valid_email_from_db,
    create_refresh_token,
    decode_token,
    add_user_to_db,
    check_user_db,
    get_user_data,
    change_password,
    CREDENTIALS_EXCEPTION,
)
from passlib.hash import pbkdf2_sha256
from oauth import oauth
from utils import redirect_uri, make_html_response

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
    # request.session.pop("user", None)
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


##############################################################


@auth_app.post("/register")
async def register(user: User):
    # Pydantic model to dictionary explicit conversion
    user_data = {}
    user_data["name"] = user.name
    user_data["email"] = user.email
    user_data["password"] = pbkdf2_sha256.using(salt_size=0).hash(user.password)
    response = await add_user_to_db(user_data)
    return JSONResponse(
        {
            "result": True,
            "user_id": response["result"],
            "email": user_data["email"],
            "password": user_data["password"],
        }
    )


@auth_app.post("/loginlocal")
async def loginlocal(form: Login_form):
    print(form)
    response_json = await check_user_db(
        form.email, pbkdf2_sha256.using(salt_size=0).hash(form.password)
    )
    if "error" in response_json:
        return JSONResponse({"authenticationSuccess?": False})
    else:
        user_id = response_json["result"]["id"]
        access_token = create_token(form.email)
        refresh_token = create_refresh_token(form.email)
        return HTMLResponse(make_html_response(user_id, access_token, refresh_token))


@auth_app.post("/changepassword")
async def changepassword(form: Pass_change_form):
    response = await change_password(
        form.email,
        pbkdf2_sha256.using(salt_size=0).hash(form.old_password),
        pbkdf2_sha256.using(salt_size=0).hash(form.new_password),
    )
    return JSONResponse(
        {
            "result": response[
                "result"
            ]  # true if change success, Error if pass didn't match
        }
    )
