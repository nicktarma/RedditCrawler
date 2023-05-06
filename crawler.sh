
#!/bin/bash

# Prompt the user to enter the subreddit name
echo "Enter subreddit name:"
read subreddit_name

# Prompt the user to enter the output filename
echo "Enter output filename:"
read output_filename

# Run the Python script with the specified subreddit and output filename
python reddit_script.py $subreddit_name $output_filename