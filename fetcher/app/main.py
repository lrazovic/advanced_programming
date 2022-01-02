import feedparser
from jsonrpcserver import method, Success, serve, Error


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
                temp["summary"] = post.summary
            except:
                pass
            post_list.append(temp)
        posts_details["posts"] = post_list
        return posts_details  # returning the details
    else:
        return None


@method
def retrive_information(
    feed_url: str = "http://www.repubblica.it/rss/homepage/rss2.0.xml",
):
    data = get_posts_details(rss=feed_url)
    if data:
        return Success(data)
    else:
        return Error()


if __name__ == "__main__":
    serve(port=5002)
