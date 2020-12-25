from flask import Flask, request, redirect, render_template
import requests
import json
from urllib.parse import quote
from spotify import track_current_song
from genius import get_lyrics

# INPUT CLIENT ID HERE
CLIENT_ID = ''
# INPUT CLIENT SECRET HERE
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:3000/callback'
SCOPES = 'user-read-private user-read-currently-playing user-read-playback-state'

AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize'
TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

app = Flask(__name__)

# Auth endpoint
@app.route('/')
def index():
  authentication_url = (AUTH_ENDPOINT +
  '?response_type=code&client_id=' + CLIENT_ID +
  '&scope=' + quote(SCOPES) +
  '&redirect_uri=' + quote(REDIRECT_URI))
  
  return redirect(authentication_url)

# Callback endpoint
@app.route('/callback')
def callback():
  payload = {
    'grant_type': 'authorization_code',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'code': str(request.args['code']),
    'redirect_uri': REDIRECT_URI,
  }

  # Obtain access and refresh tokens
  res = (requests.post(TOKEN_ENDPOINT, payload)).json()
  
  ACCESS_TOKEN = res['access_token']
  # REFRESH_TOKEN = res['refresh_token']
  # EXPIRES_IN = res['expires_in']
  
  global options
  options = {'Authorization' : 'Bearer ' + ACCESS_TOKEN}

  return redirect('/home')

@app.route('/home')
def home():
  return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
  song_data = track_current_song(options)
  song_data['lyrics'] = get_lyrics(song_data['name'], song_data['artists'][0]['name'])

  return render_template('index.html', name=song_data['name'], artist=song_data['artists'][0]['name'], 
    date=song_data['date'], pop=song_data['pop'], lyrics=song_data['lyrics'])

if __name__ == "__main__":
  app.run(port=3000)
