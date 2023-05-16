from flask import Flask, redirect, request
import tweepy
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Twitter Analytics!'

@app.route('/authorize')
def authorize():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    try:
        redirect_url = auth.get_authorization_url()
        return redirect(redirect_url)
    except tweepy.TweepError:
        return 'Error! Failed to get request token.'

@app.route('/callback')
def callback():
    verifier = request.args.get('oauth_verifier')
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.get_access_token(verifier)
    # Save these tokens for later use
    return 'Successfully authorized!'

if __name__ == '__main__':
    app.run()
