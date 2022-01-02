from fastapi import FastAPI
from . import connection
from bson import ObjectId
from schematics.models import Model
from schematics.types import StringType, EmailType
import httpx
from jsonrpcclient.requests import request_uuid

# -----------------------------------------MODEL DEFINITION


class User(Model):
    user_id = ObjectId()
    email = EmailType(required=True)
    name = StringType(required=True)
    password = StringType(required=True)


# An instance of class User
newuser = User()

# funtion to create and assign values to the instanse of class User created
def create_user(email, username, password):
    newuser.user_id = ObjectId()
    newuser.email = email
    newuser.name = username
    newuser.password = password
    return dict(newuser)


# -----------------------------------------WEB SERVER

app = FastAPI()

# Our root endpoint
@app.get("/api")
async def index():
    return {"message": "Hello World!"}


# Signup endpoint with the POST method
@app.post("/api/{email}/{username}/{password}")
async def signup(email, username: str, password: str):
    user_exists = False
    data = create_user(email, username, password)

    # Covert data to dict so it can be easily inserted to MongoDB
    dict(data)

    # Checks if an email exists from the collection of users
    if connection.db.users.count_documents({"email": data["email"]}) > 0:
        user_exists = True
        print("User Exists")
        return {"message": "User Exists"}
    # If the email doesn't exist, create the user
    elif user_exists == False:
        connection.db.users.insert_one(data)
        return {
            "message": "User Created",
            "email": data["email"],
            "name": data["name"],
            "pass": data["password"],
        }


@app.get("/api/summary")
async def summary():
    response = httpx.post(
        "http://analysis.dev:5001/",
        json=request_uuid(
            "summarize",
            params=[
                "Harry Potter is a series of seven fantasy novels written by British author J. K. Rowling."
            ],
        ),
    )
    return {"message": response.json()}


# -----------------------------------------TEST
@app.get("/api/items/{item_id}")
async def read_item(item_id, q=None):
    return {"item_id": item_id, "q": q}


# -----------------------------------------FETCHER MODULE

@app.get("/api/getnews")
async def call_fetcher():
    return fetcher.retrive_information()
