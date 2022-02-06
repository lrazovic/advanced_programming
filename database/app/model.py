from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

base = declarative_base()


class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
