# Able to read all the posts when specified a subreddit
import json
import praw
reddit = praw.Reddit("bot1")

# print(reddit.read_only)

reddit.read_only = True

# A dictionary of every post
postDict = {}



top = reddit.subreddit("personalfinance").new(limit=2)
for post in top:
    
    # A dictionary of all the infromation for the post
    # Resets after every pass 
    postInfo = {}

    postInfo["title"] = post.title
    # print(post.title)
    postInfo["body"] = post.selftext
    # print(post.selftext)
    postInfo["url"] = post.url
    # print(post.url)
    postInfo["permalink"] = post.permalink
    # print(post.permalink)

    postDict[post.id] = postInfo

for post in postDict:
  print(post)
  print (redditPostToJSONconv(post.title, post.body, post.url, post.permalink))


def redditPostToJSONconv (title, body, url, permalink):
  title_str = "title: %s"%title
  body_str = "body: %s"%title
  url_str = "url: %s"%title
  permalink_str = "permalink: %s"%title

  combined_str = "{" + title_str + ", " + body_str + ", " + url_str + ", " + permalink_str + "}"
  return json.dump(combined_str)
    