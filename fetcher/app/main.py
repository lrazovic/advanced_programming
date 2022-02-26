import feedparser
import logging
from jsonrpcserver import method, Success, serve, Error
from bs4 import BeautifulSoup

logging.getLogger().setLevel(logging.INFO)


def get_posts_details(rss, limit):
    try:
        blog_feed = feedparser.parse(rss)
        # getting lists of blog entries
        posts = blog_feed.entries[:limit]
        # dictionary for holding posts details
        posts_details = {
            "Blog title": blog_feed.feed.title,
            "Blog link": blog_feed.feed.link,
        }
        post_list = []
        for post in posts:
            temp = dict()
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
        return Success(posts_details)
    except Exception as e:
        return Error(f"Error in getting posts details: {e}")


@method
def retrive_information(feed_url: str, limit: int):
    logging.info(f" * RSS requests for: {feed_url}")
    return get_posts_details(feed_url, limit)


if __name__ == "__main__":
    PORT = 5002
    serve(port=PORT)
