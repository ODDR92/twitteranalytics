# twitter_api.py
import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_auth():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    return auth

def get_redirect_url(auth):
    try:
        redirect_url = auth.get_authorization_url()
        return redirect_url
    except tweepy.TweepError:
        return None

def get_access_token(auth, verifier):
    try:
        auth.get_access_token(verifier)
        return auth.access_token, auth.access_token_secret
    except tweepy.TweepError as e:
        print(f"Error! Failed to get access token: {e}")
        return None, None
