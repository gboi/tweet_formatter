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
css_file = os.path.join(THIS_FOLDER, 'image.css')
png_file = os.path.join(THIS_FOLDER, 'tweet.png')
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
        processed_html = file.read()
    processed_html = process_html(processed_html, user_image, screen_name, message, date)
    with open(css_file, "r") as file:
        processed_css = file.read()
    processed_css = process_css(processed_css, background_image)
    with tempfile.TemporaryFile(mode='w+t', delete=False) as tmp_css:
        tmp_css.writelines(processed_css)
    
    if(debug):
        print(processed_html)
        print(process_css)
    imgkit.from_string(processed_html, png_file, css=tmp_css.name)
    
def process_html(html, user_image, screen_name, message, date):
    message = message.replace("\n", "<br/>")
    html = html.replace("%PROFILE_ICON%", user_image)
    html = html.replace("%SCREEN_NAME%", screen_name)
    html = html.replace("%TWEET_CONTENT%", message)
    date_string = '{:%A %m/%d/%Y %I:%M%p}'.format(date)
    # Timezone doesn't work
    # date_string = '{:%A %m/%d/%Y %I:%M%p %Z}'.format(date)
    html = html.replace("%TWEET_DATE%", date_string)
    return html

def process_css(css, background_image):
    css = css.replace("%BACKGROUND_IMAGE%", background_image)
    # css = css.replace("%FONT_PATH%", font_file)
    return css

def convert_image(image):
    with open(image, "rb") as file:
        image_string = base64.b64encode(file.read())
    return image_string.decode('utf-8')