import feedparser
import json


def get_posts_details(rss=None):
    
    """
    Take link of rss feed as argument
    """
    if rss is not None:
        blog_feed = blog_feed = feedparser.parse(rss)  
        # getting lists of blog entries
        posts = blog_feed.entries  
        # dictionary for holding posts details
        posts_details = {"Blog title" : blog_feed.feed.title,
                        "Blog link" : blog_feed.feed.link}  
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
        return posts_details # returning the details
    else:
        return None 
if __name__ == "__main__":
  feed_url = "http://www.repubblica.it/rss/homepage/rss2.0.xml"
  data = get_posts_details(rss = feed_url)
  if data:
    # printing as a json string
    print(json.dumps(data, indent=2)) 
  else:
    print("None")