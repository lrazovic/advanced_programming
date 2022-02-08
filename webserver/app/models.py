from pydantic import BaseModel


class NewsText(BaseModel):
    body: str = "A very long text, mainly written in English"


class NewsFeed(BaseModel):
    url: str = "http://feeds.bbci.co.uk/news/world/rss.xml"
    limit: int = 10
