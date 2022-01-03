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