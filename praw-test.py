
#https://gilberttanner.com/blog/scraping-redditdata/
#https://www.reddit.com/prefs/apps


import praw
import json
import urllib3
import bs4 as BeautifulSoup

#Got the following code off of stack overflow and repurposed it to suit the program.
def getUrlTitle(title):
    soup = BeautifulSoup(urllib3.urlopen(title))
    return(soup.title.string)


def getURLlink(jsonObj):
    urls = []
    x = 0
    while(x <= len(jsonObj)): 
      var1 = jsonObj.find('](http', x, )
      var2 = jsonObj.find(')', var1+1, )
      ans = jsonObj[var1+1: var2]
      ans += "http"
      x = var2
      urls.append(ans)
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
# A list to store external link's titles
externTitles = []

for post in ml_subreddit.hot(limit=2):
    
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

    # for link in urls:
    #     externTitles.append(getUrlTitle(link))
        
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


print("Len after hot posts: ", len(postIDs))

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

