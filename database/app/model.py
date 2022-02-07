from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Sequence, String

base = declarative_base()


class User(base):
    __tablename__ = "user"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    email = Column(String)
    name = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
