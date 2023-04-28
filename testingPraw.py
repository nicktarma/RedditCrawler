# Able to read all the posts when specified a subreddit

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
