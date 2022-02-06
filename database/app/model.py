from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

base = declarative_base()


class User(base):
    __tablename__ = "user"

    email = Column(String, primary_key=True)
    name = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
