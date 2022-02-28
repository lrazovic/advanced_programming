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


@auth_app.get("/logout", summary="Pop the user session")
async def logout(request: Request):
    # request.session.pop("user", None)
    return RedirectResponse(url="/")


@auth_app.post("/refresh", summary="Use the refresh token to create a new access token")
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


@auth_app.post(
    "/register",
    summary="Add to the db a new user registered with traditional credentials",
)
async def register(user: User):
    # Pydantic model to dictionary explicit conversion
    user_data = {}
    user_data["name"] = user.name
    user_data["email"] = user.email
    # TODO: Use BCrypt instead of SHA256
    # Reference: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html
    user_data["password"] = user.password
    response = await add_user_to_db(user_data)
    return JSONResponse(
        {
            "result": True,
            "user_id": response["result"],
            "email": user_data["email"],
        }
    )


@auth_app.post(
    "/loginlocal",
    summary="Manage the authentication process with the traditional credentials",
)
async def loginlocal(form: Login_form):
    response_json = await check_user_db(form.email, form.password)
    if "error" in response_json:
        return JSONResponse({"authenticationSuccess?": False})
    else:
        user_id = response_json["result"]["id"]
        access_token = create_token(form.email)
        refresh_token = create_refresh_token(form.email)
        return JSONResponse(
            {
                "user_id": user_id,
                "jwt": access_token,
                "refresh": refresh_token,
            }
        )


@auth_app.post(
    "/changepassword",
    summary="Change the currently authenticthed user's password in the db",
)
async def changepassword(form: Pass_change_form):
    response = await change_password(
        form.email,
        form.old_password,
        form.new_password,
    )
    # Returns `true` if change success, `Error` if `old_password` didn't match
    return JSONResponse({"result": response["result"]})
