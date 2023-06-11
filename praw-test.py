#https://www.reddit.com/prefs/apps


import praw
import json
import requests
from bs4 import BeautifulSoup
import re
import sys

# Variable that changes the number of posts collected
limit_val = 200


#This function is used to utilize the link to extract the titles for the websites within the body.
def getUrlTitle(link):
    
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        ret_title = soup.title.string
        if not isinstance(ret_title, str):
            raise AttributeError
    except:
        return ''



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
    return urls

def redditCrawler(subreddit_name, outputfile_name):

    reddit = praw.Reddit(client_id='YAgCOYnP96vukl8AKBhOzw',
                    client_secret='SCyJkjfbB24ZkGxt-wGm0JcT2xXKqw',
                    user_agent='praw-test')

    # This writes the data in the required json format
    posts = []

    # Maintaining a list of ID's to cross-verify
    postIDs = set([])

    ml_subreddit = reddit.subreddit(subreddit_name)

    # Tracks the number of posts parsed through
    postNumber = 0

    # The opening bracket of the list
    with open(outputfile_name, 'a') as file:
        file.write('[')


    '''
    -----------------------------
    Parsing through the top posts
    -----------------------------
    '''
    for post in ml_subreddit.top(limit=limit_val):

        print("We're on post: ", postNumber)
        postNumber+=1
        # A list to store external link's titles
        externTitles = []
        
        # Check if the post already exists
        if post.id in postIDs:
            continue
        
        # If not, add it to the ID list
        postIDs.add(post.id)

        # Adding the all the comments from every post
        post.comments.replace_more(limit=None)
        comment_list = []
        if post.num_comments > 0:
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

        # Write all the posts into data.json
        with open(outputfile_name, 'a') as file:
            json.dump(data, file)
    '''
    -----------------------------
    Parsing through the hot posts
    -----------------------------
    '''
    for post in ml_subreddit.hot(limit=limit_val):

        print("We're on post: ", postNumber)
        postNumber+=1
        # A list to store external link's titles
        externTitles = []
        
        # Check if the post already exists
        if post.id in postIDs:
            continue
        
        # If not, add it to the ID list
        postIDs.add(post.id)

        # Adding the all the comments from every post
        post.comments.replace_more(limit=None)
        comment_list = []
        if post.num_comments > 0:
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

        # Write all the posts into data.json
        with open(outputfile_name, 'a') as file:
            json.dump([data], file)
    '''
    -----------------------------
    Parsing through the new posts
    -----------------------------
    '''
    for post in ml_subreddit.new(limit=limit_val):

        print("We're on post: ", postNumber)
        postNumber+=1
        # A list to store external link's titles
        externTitles = []
        
        # Check if the post already exists
        if post.id in postIDs:
            continue
        
        # If not, add it to the ID list
        postIDs.add(post.id)

        # Adding the all the comments from every post
        post.comments.replace_more(limit=None)
        comment_list = []
        if post.num_comments > 0:
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

        # Write all the posts into data.json
        with open(outputfile_name, 'a') as file:
            json.dump(data, file)    

    # The closing bracket of the list
    with open(outputfile_name, 'a') as file:
        file.write(']')



def main(input_method=None):

    if input_method == 'bash':
        subreddit_name = sys.argv[1]
        outputfile_name = sys.argv[2]
    else:
        subreddit_name = input("Please enter the name of the subreddit you would like to crawl Ex. (personalfinance): ")
        outputfile_name = input("Please enter the name of the JSON file you would like to store the output into Ex. (data.json) : ")

    redditCrawler(subreddit_name, outputfile_name)

if __name__ == "__main__":
    main()
    

