#!/bin/bash

#install necessary libraries
pip3 install praw urllib3 beautifulsoup4
#python -m pip install urllib3
#running the script
#nohup runs it in the background
#> /dev/null ignores output
nohup python3 praw-test.py > /dev/null 2>&1 &