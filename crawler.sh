#!/bin/bash

# install necessary libraries
pip3 install praw urllib3 beautifulsoup4

# running the script
# nohup runs it in the background
#> /dev/null ignores output

nohup python3 praw-test.py $1 $2 > /dev/null 2>&1 &