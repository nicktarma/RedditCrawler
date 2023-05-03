#https://gilberttanner.com/blog/scraping-redditdata/
#https://www.reddit.com/prefs/apps


import praw
import json

reddit = praw.Reddit(   client_id='YAgCOYnP96vukl8AKBhOzw',
                        client_secret='SCyJkjfbB24ZkGxt-wGm0JcT2xXKqw',
                        user_agent='praw-test')

import pandas as pd
posts = []
ml_subreddit = reddit.subreddit('personalfinance')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.title, post.score,        post.id,       post.subreddit, 
                  post.url,   post.num_comments, post.selftext, post.created])
posts = pd.DataFrame(posts,columns=[0, 1, 2, 3, 4, 5, 6, 7])
# 0,       1,       2,    3,           4,     5,              6,      7,   
#'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'


'''
df = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]})
df = df.reset_index()  # make sure indexes pair with number of rows

for index, row in df.iterrows():
    print(row['c1'], row['c2'])
    '''

for index, row in posts.iterrows():
    for i in range(0,7):
        print("Index number ", index, row[i])
        #with open('data.json', 'w') as file:
            #file.write(json.dump(row[i]))

# print("Shape: ", posts.shape)

#for post in posts:
 #   with open('data.json', 'w') as file:
        # file.write(json.dump(post))
        #file.write(json.dump(post,file))
        #file.write(post.to_json())
'''
for i in range(1, len(posts)):
    print("Post type: ", type(post.split()))
    print("Post: ",post)
    for cat in post:
        print("Cat: ",cat)
    with open('data.json', 'w') as file:
        json_string = json.dump(post.split(), file)
        print(json_string)

# print(json_posts)
'''
'''
def redditPostToJSONconv (title, body, url, permalink):
  title_str = "title: %s"%title
  body_str = "body: %s"%title
  url_str = "url: %s"%title
  permalink_str = "permalink: %s"%title

  combined_str = "{" + title_str + ", " + body_str + ", " + url_str + ", " + permalink_str + "}"
  return json.dump(combined_str)
'''