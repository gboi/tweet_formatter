import tweepy
import os
import sys
import datetime
import imgkit
import base64
import shutil
import tempfile
import urllib.request

consumer_key = "4wG7s5w7QxGY4SDQYS0Ij5tC3"
consumer_secret = "vjG0G4gDxjl7HvMapgJRLAF2FRAdENL0FczIjo3l7nYHUy8Hsz"
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
html_file = os.path.join(THIS_FOLDER, 'image.html')
jpg_file = os.path.join(THIS_FOLDER, 'image.jpg')
bg_file = os.path.join(THIS_FOLDER, 'bg.jpg')
    
def get_image(tweet_id, debug):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    message = tweet.full_text
    date = tweet.created_at
    screen_name = tweet.user.screen_name
    user = api.get_user(tweet.user.id)
    user_image_url = tweet.user.profile_image_url_https
    user_image_url = user_image_url.replace("normal", "400x400")
    
    if(debug):
        print(message)
        print(date)
        print(screen_name)
        print(user_image_url)
        
    background_image = convert_image(bg_file)
        
    with urllib.request.urlopen(user_image_url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
    user_image = convert_image(tmp_file.name)
        
    with open(html_file, "r") as file:
        html = file.read()
    html = process_html(html, user_image, screen_name, message, date, background_image)
    
    if(debug):
        print(html)
    imgkit.from_string(html, jpg_file)
        
def process_html(html, user_image, screen_name, message, date, background_image):
    html = html.replace("%PROFILE_ICON%", user_image)
    html = html.replace("%SCREEN_NAME%", screen_name)
    html = html.replace("%TWEET_CONTENT%", message)
    html = html.replace("%BACKGROUND_IMAGE%", background_image)
    date_string = '{:%A %m/%d/%Y %I:%M%p}'.format(date)
    # Timezone doesn't work
    # date_string = '{:%A %m/%d/%Y %I:%M%p %Z}'.format(date)
    html = html.replace("%TWEET_DATE%", date_string)
    return html

def convert_image(image):
    with open(image, "rb") as file:
        image_string = base64.b64encode(file.read())
    return image_string.decode('utf-8')