from fastapi import FastAPI
from . import connection
from bson import ObjectId
from schematics.models import Model
from schematics.types import StringType, EmailType

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
@app.get("/")
def index():
    return {"message": "Hello World!"}

# Signup endpoint with the POST method
@app.post("/api/{email}/{username}/{password}")
def signup(email, username: str, password: str):
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

# -----------------------------------------TEST
@app.get("/items/{item_id}")
def read_item(item_id, q = None):
    return {"item_id": item_id, "q": q}

# -----------------------------------------FETCHER MODULE
import fetcher.main as fetcher

@app.get("/getNews")
def call_fetcher():
    return fetcher.retrive_information()
