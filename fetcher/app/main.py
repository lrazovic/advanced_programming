import feedparser
from jsonrpcserver import method, Success, serve, Error
from bs4 import BeautifulSoup

import logging

logging.getLogger().setLevel(logging.INFO)

#FIXME
# Schifoso codice scritto da Antonio
############################################################################################################################################################
import psycopg
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, true
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    #TODO Autgeneration id
    id = Column(Integer, primary_key=True)
    
    iss = Column(String)
    azp = Column(String)
    aud = Column(String)
    sub = Column(String)
    email = Column(String)
    emailVerfied = Column(String)
    atHash = Column(String)
    nonce = Column(String)
    name = Column(String)
    picture = Column(String)
    givenName = Column(String)
    familyName = Column(String)
    locale = Column(String)
    iat = Column(String)
    exp = Column(String)
    
    #TODO
    # def __repr__(self):
    #     return "<Book(title='{}', author='{}', pages={}, published={})>"\
    #             .format(self.title, self.author, self.pages, self.published)

def createUserRelation(dto: User):
    engine = sqlalchemy.create_engine('postgresql+pg8000://pguser:pguser@localhost:5432/pgdb')
    print(engine)

    Base.metadata.create_all(engine)

def addUser(dto: User):
    engine = sqlalchemy.create_engine('postgresql+pg8000://pguser:pguser@localhost:5432/pgdb')

    Session = sessionmaker(bind=engine)
    s = Session()

    s.add(dto)
    s.commit()

    s.close()

    return true
    
@method
def crud_test(dto: User):
    logging.info(f"DTO received: {dto}")
    r = addUser(dto)
    if r:
        return Success()
    else:
        return Error()
############################################################################################################################################################


def get_posts_details(rss=None, last=10):
    if rss is not None:
        blog_feed = feedparser.parse(rss)
        # getting lists of blog entries
        posts = blog_feed.entries[:last]
        # dictionary for holding posts details
        posts_details = {
            "Blog title": blog_feed.feed.title,
            "Blog link": blog_feed.feed.link,
        }
        post_list = []
        for post in posts:
            temp = dict()
            # if any post doesn't have information then throw error
            try:
                temp["title"] = post.title
                temp["link"] = post.link
                temp["author"] = post.author
                temp["time_published"] = post.published
                temp["tags"] = [tag.term for tag in post.tags]
                temp["authors"] = [author.name for author in post.authors]
                temp["summary"] = BeautifulSoup(post.summary, "lxml").text
            except:
                pass
            post_list.append(temp)
        posts_details["posts"] = post_list
        return posts_details  # returning the details
    else:
        return None


@method
def retrive_information(
    feed_url: str = "http://feeds.bbci.co.uk/news/world/rss.xml",
):
    logging.info(f" * RSS requests for: {feed_url}")
    data = get_posts_details(rss=feed_url)
    if data:
        return Success(data)
    else:
        return Error()


if __name__ == "__main__":
    PORT = 5002
    serve(port=PORT)
