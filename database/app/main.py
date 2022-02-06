from jsonrpcserver import method, Success, serve, Error, Result
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User
from model import base
import logging
import os

logging.getLogger().setLevel(logging.INFO)


def addUser(dto):
    try:
        session = Session()
        user = User(
            name=dto["name"],
            email=dto["email"],
            access_token=dto["access_token"],
            refresh_token=dto["refresh_token"],
        )
        session.add(user)
        session.commit()
        session.close()
        logging.info("User added")
        return True
    except Exception as e:
        logging.error(e)
        return False


@method
def add_user_to_db(dto) -> Result:
    if addUser(dto):
        return Success("pong")
    else:
        return Error(1, "There was a problem")


if __name__ == "__main__":
    PORT = 5003
    if "DEV" in os.environ:
        db_string = "postgresql://advanced_programming:pguser@localhost:5432/advanced_programming"
    else:
        db_string = "postgresql://advanced_programming:pguser@postgres:5432/advanced_programming"
    db = create_engine(db_string)
    Session = sessionmaker(db)
    base.metadata.create_all(db)
    logging.info("Connected to DB: {}".format(db_string))
    serve(port=PORT)
