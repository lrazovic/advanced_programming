from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Sequence, String, ForeignKey
from sqlalchemy.orm import relationship

base = declarative_base()


class User(base):
    __tablename__ = "user"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    email = Column(String)
    name = Column(String)
    # access_token = Column(String)
    # refresh_token = Column(String)
    password = Column(String)
    rssFeeds = relationship("RssFeed", cascade="all, delete, delete-orphan")


class RssFeed(base):
    __tablename__ = "rss_feed"

    id = Column(Integer, Sequence("rss_feed_id_seq"), primary_key=True)
    url = Column(String)
    rank = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))


def RssFeedDtoToEntity(dto):
    return RssFeed(url=dto["url"], rank=dto["rank"])


def RssFeedDtoListToEntityList(dtoList):
    entityList: List[RssFeed] = []

    for dto in dtoList:
        entityList.append(RssFeedDtoToEntity(dto))

    return entityList
