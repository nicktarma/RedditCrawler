#https://gilberttanner.com/blog/scraping-redditdata/
#https://www.reddit.com/prefs/apps


import praw
import json
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

# This function is used to utilize the link to extract the titles for the websites within the body.
def getUrlTitle(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    ret_title = soup.title.string

    # print("Inside soup: " , ret_title) # Testing

    # Checks to see whether we actually got the title (kinda slow but easy to understand)
    if "403" in ret_title:
        return ''
    elif "404" in ret_title:
        return ''
    elif "denied" in ret_title.lower():
        return ''
    elif "not" and "found" in ret_title.lower():
        return ''
    elif "too" and "many" and "requests" in ret_title.lower():
        return ''
    else:
        return(ret_title)


# This function helps gather links from the body
def getURLlink(jsonObj):
    urls = re.findall (r'\]\((http.*?)\)', jsonObj)
    urls = [url + 'http' for url in urls]
    # urls = ["https://en.wikipedia.org/wiki/Badge_Man"]
    return urls

reddit = praw.Reddit(client_id='YAgCOYnP96vukl8AKBhOzw',
                client_secret='SCyJkjfbB24ZkGxt-wGm0JcT2xXKqw',
                user_agent='praw-test')

# This writes the data in the required json format
posts = []

# Maintaining a list of ID's to cross-verify
postIDs = set([])

ml_subreddit = reddit.subreddit('personalfinance')

'''
-----------------------------
Parsing through the hot posts
-----------------------------
'''
for post in ml_subreddit.hot(limit=100):

    # A list to store external link's titles
    externTitles = []
    
    # Check if the post already exists
    if post.id in postIDs:
        continue
    
    # If not, add it to the ID list
    postIDs.add(post.id)

    # Adding the all the comments from every post
    post.comments.replace_more(limit=None)
    if post.num_comments > 0:
        comment_list = []
        for comment in post.comments.list():
            comment_list.append(comment.body)

    # Parse through the body of the post to look for links
    urls = getURLlink(post.selftext)

    # Getting the page's titles for given links
    for link in urls:
        title = getUrlTitle(link)
        if title != '':
            externTitles.append(title)
        
    # Adding all of the post's characteristics
    data = {
        "title": post.title,
        "score": post.score,
        "id": post.id,
        "subreddit": post.subreddit.display_name,
        "url": post.url,
        "num_comments": post.num_comments,
        "body": post.selftext,
        "created": post.created_utc,
        "comments" : comment_list,
        "External Link Titles" : externTitles
    }
    posts.append(data)

# Testing
print("Len after hot posts: ", len(postIDs))
print(externTitles)


'''
-------------------------------
Parsing through the top posts
------------------------------

# A list to store external link's titles
externTitles = []

for post in ml_subreddit.top(limit=10):
    
    # Check if the post already exists
    if post.id in postIDs:
        continue
    
    # If not, add it to the ID list
    postIDs.add(post.id)

    # Adding the all the comments from every post
    post.comments.replace_more(limit=None)
    if post.num_comments > 0:
        comment_list = []
        for comment in post.comments.list():
            comment_list.append(comment.body)
        
        # Adding all of the post's characteristics
        data = {
            "title": post.title,
            "score": post.score,
            "id": post.id,
            "subreddit": post.subreddit.display_name,
            "url": post.url,
            "num_comments": post.num_comments,
            "body": post.selftext,
            "created": post.created_utc,
            "comments" : comment_list
        }
        posts.append(data)


print("Len after top posts: ", len(postIDs))
'''


# Write all the posts into data.json
with open('data.json', 'w') as file:
    json.dump(posts, file)


# This shows us that we could access the data 
# with open('data.json', 'r') as file:
#     data = json.load(file)
#     print(data[8]["score"])

