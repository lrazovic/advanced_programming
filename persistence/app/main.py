from jsonrpcserver import method, Success, serve, Error, Result
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, subqueryload
from model import base, User, RssFeedDtoListToEntityList
from fastapi.encoders import jsonable_encoder
from passlib.hash import bcrypt
import traceback
import logging
import os

logging.getLogger().setLevel(logging.INFO)

if "DEV" in os.environ:
    db_string = "postgresql+pg8000://advanced_programming:pguser@localhost:5432/advanced_programming"
else:
    db_string = "postgresql+pg8000://advanced_programming:pguser@postgres:5432/advanced_programming"
db = create_engine(db_string)
Session = sessionmaker(db)
base.metadata.create_all(db)


def getUserById(id):
    try:
        session = Session()
        user = session.query(User).options(subqueryload(User.rssFeeds)).get(id)
        session.commit()

        logging.info(f"\nRetrived User with id: {user.id}\n")

        return True, jsonable_encoder(user)
    except Exception as e:
        logging.error(traceback.print_exc())
        message = e
        return False, message


def checkUserByEmailAndPassword(email, password):
    try:
        session = Session()
        user = (
            session.query(User)
            .options(subqueryload(User.rssFeeds))
            .filter(User.email == email)
            .first()
        )
        session.commit()
        if user != None and bcrypt.verify(password, user.password):
            logging.info(f"\nRetrived User with id: {user.id}\n")
            return True, jsonable_encoder(user)
        else:
            return False, "Check not passed."

    except Exception as e:
        logging.error(traceback.print_exc())
        message = e
        return False, message


def addUser(dto):
    try:
        session = Session()
        user = session.query(User).filter(User.email == dto["email"]).first()
        if user != None:
            session.commit()
            return True, user.id

        if "password" in dto:
            newUser = User(
                email=dto["email"], name=dto["name"], password=bcrypt.hash(dto["password"])
            )
        else:
            newUser = User(email=dto["email"], name=dto["name"])
        session.add(newUser)
        session.commit()

        return True, newUser.id
    except Exception as e:
        logging.error(e)
        message = e
        return False, message


def updateUserRssFeeds(userId, feedsDto):
    try:
        session = Session()
        targetUser = session.query(User).get(userId)
        targetUser.rssFeeds.clear()
        targetUser.rssFeeds.extend(RssFeedDtoListToEntityList(feedsDto["rssFeeds"]))
        session.commit()

        message = (
            f"User with id {targetUser.id} updated: new list of associated RSS feeds"
        )
        return True, message
    except Exception as e:
        logging.error(traceback.print_exc())
        message = e
        return False, message


def deleteUserById(id):
    try:
        session = Session()
        user = session.query(User).options(subqueryload(User.rssFeeds)).get(id)
        userId = user.id
        session.delete(user)
        session.commit()

        msg = f"\nDeleted User with id: {userId}\n"
        logging.info(msg)

        return True, msg
    except Exception as e:
        logging.error(traceback.print_exc())
        message = e
        return False, message


#########


def updateUserPass(email, oldPass, newpassword):
    try:
        with Session.begin() as session:
            # Check if tuple (email,password) is in the database
            user = session.query(User).filter_by(email=email).first()
            if user and bcrypt.verify(oldPass, user.password):
                user.password = bcrypt.hash(newpassword)
                session.commit()
                message = "True"
                return True, message
            else:
                message = "False"
                return True, message
    except Exception as e:
        logging.error(e)
        message = e
        return False, message


########
# CRUD Operations on User entity


@method
def getUserUserId(userId) -> Result:
    ok, result = getUserById(userId)
    if ok:
        return Success(result)
    else:
        return Error(1, result)


@method
def add_user_to_db(dto) -> Result:
    status, message = addUser(dto)
    if status:
        return Success(message)
    else:
        return Error(1, message)


@method
def update_user_rss_feeds(userId, feedsDto) -> Result:
    status, message = updateUserRssFeeds(userId, feedsDto)
    if status:
        return Success(message)
    else:
        return Error(1, message)


@method
def deleteUserUserId(userId) -> Result:
    ok, result = deleteUserById(userId)
    if ok:
        return Success(result)
    else:
        return Error(1, result)


# Security check involved in the oAuth2 flow
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


# Just for checking if the db is alive
@method
def read_db() -> Result:
    with Session.begin() as session:
        users = session.query(User)
    names = {}
    for user in users:
        names[user.email] = (user.id, user.name)
    return Success(names)


################################


@method
def valid_user_from_db(email, password) -> Result:
    ok, result = checkUserByEmailAndPassword(email, password)
    if ok:
        return Success(result)
    else:
        return Error(1, result)


def getUser(email):
    try:
        session = Session()
        user = (
            session.query(User)
            .options(subqueryload(User.rssFeeds))
            .filter(User.email == email)
            .first()
        )
        session.commit()

        logging.info(f"\nRetrived User with id: {user.id}\n")

        return True, jsonable_encoder(user)
    except Exception as e:
        logging.error(traceback.print_exc())
        message = e
        return False, message


@method
def getLoggedUser(email) -> Result:
    ok, result = getUser(email)
    if ok:
        return Success(result)
    else:
        return Error(1, result)


@method
def update_user_pass(email, oldPass, newpassword) -> Result:
    status, message = updateUserPass(email, oldPass, newpassword)
    return Success(message)


################################

if __name__ == "__main__":
    PORT = 5003
    logging.info("Connected to DB: {}".format(db_string))
    serve(port=PORT)
