from typing import List
from pydantic import BaseModel


class NewsText(BaseModel):
    body: str = "A very long text, mainly written in English"


class RssFeedDto(BaseModel):
    url: str = "http://feeds.bbci.co.uk/news/world/rss.xml"
    rank: int = 1


class UserRssFeedsDto(BaseModel):
    user_id: int = 1
    rssFeeds: List[RssFeedDto]


###########################################


class User(BaseModel):
    name: str = "User name"
    email: str = "User email"
    password: str = "User password"


class Login_form(BaseModel):
    email: str = "User email"
    password: str = "User password"


class Pass_change_form(BaseModel):
    email: str = "User email"
    old_password: str = "Old user password"
    new_password: str = "New user password"
