
#https://gilberttanner.com/blog/scraping-redditdata/
#https://www.reddit.com/prefs/apps


import praw
import json

reddit = praw.Reddit(   client_id='YAgCOYnP96vukl8AKBhOzw',
                        client_secret='SCyJkjfbB24ZkGxt-wGm0JcT2xXKqw',
                        user_agent='praw-test')

# This writes the datas in the required json format

posts = []
ml_subreddit = reddit.subreddit('personalfinance')
for post in ml_subreddit.hot(limit=10):
    post.comments.replace_more(limit=None)
    if post.num_comments > 0:
        comment_list = []
        for comment in post.comments.list():
            comment_list.append(comment.body)
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

with open('data.json', 'w') as file:
    json.dump(posts, file)


# This shows us that we could access the data 
with open('data.json', 'r') as file:
    data = json.load(file)
    print(data[8]["score"])