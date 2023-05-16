# app.py
from flask import Flask, redirect, request, render_template
from twitter_api import get_auth, get_redirect_url, get_access_token
import requests
import csv
import os
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/authorize')
def authorize():
    auth = get_auth()
    print(f"Auth object: {auth}")  # Debug print statement
    redirect_url = get_redirect_url(auth)
    if redirect_url:
        return redirect(redirect_url)
    else:
        return 'Error! Failed to get request token.'

@app.route('/callback')
def callback():
    verifier = request.args.get('oauth_verifier')
    print(f"Verifier: {verifier}")  # Debug print statement
    auth = get_auth()
    access_token, access_token_secret = get_access_token(auth, verifier)
    if access_token and access_token_secret:
        # Save these tokens for later use
        return 'Successfully authorized!'
    else:
        return 'Error! Failed to get access token.'

@app.route('/fetch_tweets')
def fetch_tweets():
    # Get the user's tweets from the past 30 days
    user_id = 'YOUR_USER_ID'  # Replace with the ID of the authenticated user
    bearer_token = os.getenv('BEARER_TOKEN')
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        'expansions': 'non_public_metrics',
        'start_time': (datetime.now() - timedelta(days=30)).isoformat()+'Z',
    }
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }

    response = requests.get(url, params=params, headers=headers)
    tweets = response.json()['data']

    # Write the tweets to a CSV file
    with open('tweets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet ID', 'Text', 'Impressions'])
        for tweet in tweets:
            writer.writerow([tweet['id'], tweet['text'], tweet['non_public_metrics']['impression_count']])

    return 'Successfully fetched tweets!'

if __name__ == '__main__':
    app.run()
