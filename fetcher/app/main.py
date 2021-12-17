#Feed Structure

import feedparser
NewsFeed = feedparser.parse("https://www.ilpost.it/feed")
entry = NewsFeed.entries[1]

print (entry.keys())

print ('post title: ', entry['title'])
