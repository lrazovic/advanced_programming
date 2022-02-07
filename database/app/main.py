from jsonrpcserver import method, Success, serve, Error, Result
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User
from model import base
import logging
import os

logging.getLogger().setLevel(logging.INFO)

if "DEV" in os.environ:
    db_string = (
        "postgresql+pg8000://advanced_programming:pguser@localhost:5432/advanced_programming"
    )
else:
    db_string = (
        "postgresql+pg8000://advanced_programming:pguser@postgres:5432/advanced_programming"
    )
db = create_engine(db_string)
Session = sessionmaker(db)
base.metadata.create_all(db)


def addUser(dto):
    try:
        user = User(
            email=dto["email"],
            name=dto["name"],
            access_token=dto["access_token"],
            refresh_token=dto["refresh_token"],
        )
        with Session.begin() as session:
            # Check if user already exists
            # if session.query(User).filter_by(email=dto["email"]).first():
            #     # TODO: Update user access_token and refresh_token
            #     return True, "User already exists"
            session.add(user)
        message = "User added to the DB"
        return True, message
    except Exception as e:
        logging.error(e)
        message = e
        return False, message


@method
def valid_email_from_db(email) -> Result:
    try:
        with Session.begin() as session:
            # Check if user already exists
            if session.query(User).filter_by(email=email).first():
                return Success(True)
            else:
                return Success(False)
    except Exception as e:
        logging.error(e)
        return Error(500, e)


@method
def add_user_to_db(dto) -> Result:
    status, message = addUser(dto)
    if status:
        return Success(message)
    else:
        return Error(1, message)


@method
def read_db() -> Result:
    with Session.begin() as session:
        users = session.query(User)
    names = {}
    for user in users:
        names[user.email] = user.name
    return Success(names)


if __name__ == "__main__":
    PORT = 5003
    logging.info("Connected to DB: {}".format(db_string))
    serve(port=PORT)
