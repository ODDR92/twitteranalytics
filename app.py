# app.py
from flask import Flask, redirect, request, render_template
from twitter_api import get_auth, get_redirect_url, get_access_token

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/authorize')
def authorize():
    auth = get_auth()
    redirect_url = get_redirect_url(auth)
    if redirect_url:
        return redirect(redirect_url)
    else:
        return 'Error! Failed to get request token.'

@app.route('/callback')
def callback():
    verifier = request.args.get('oauth_verifier')
    auth = get_auth()
    access_token, access_token_secret = get_access_token(auth, verifier)
    if access_token and access_token_secret:
        # Save these tokens for later use
        return 'Successfully authorized!'
    else:
        return
