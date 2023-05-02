#https://gilberttanner.com/blog/scraping-redditdata/
#https://www.reddit.com/prefs/apps


import praw

reddit = praw.Reddit(   client_id='YAgCOYnP96vukl8AKBhOzw',
                        client_secret='SCyJkjfbB24ZkGxt-wGm0JcT2xXKqw',
                        user_agent='praw-test')

import pandas as pd
posts = []
ml_subreddit = reddit.subreddit('personalfinance')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
print(posts)
