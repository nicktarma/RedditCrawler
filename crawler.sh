#!/bin/bash

echo "Please enter the name of the subreddit you would like to crawl Ex. (personalfinance): "
read subreddit_name

echo "Please enter the name of the JSON file you would like to store the output into Ex. (data.json) : "
read output_filename

python praw-test.py "$subreddit_name" "$output_filename" bash