import sys
import re
import Tweet_Formatter

def generate_image(tweet_url, debug=False):
    try:
        tweet_id = tweet_url.split('status/')[1]
        Tweet_Formatter.get_image(tweet_id, debug)
    except:
        raise IOError("Error parsing Tweet URL")

if len(sys.argv) > 3:
    raise IOError("Error: input a tweet URL | run (url) [-debug]")
elif len(sys.argv) == 1:
    tweet_url = input("Enter tweet url: ")
    generate_image(tweet_url)
else:
    for arg in sys.argv:
        if "/status/" in arg:
            url = arg
            break
    if "-debug" in sys.argv:
        generate_image(sys.argv[1], True)
    else:
        generate_image(sys.argv[1])