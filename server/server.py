from flask import Flask, request, redirect, render_template, jsonify
import requests
from urllib.parse import quote
from service import getSongInformation

# INPUT YOUR SPOTIFY CLIENT ID AND CLIENT SECRET HERE
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
# INPUT YOUR GENIUS ACCESS TOKEN HERE
GENIUS_ACCESS_TOKEN = ''

REDIRECT_URI = 'http://127.0.0.1:3000/callback'
SCOPES = 'user-read-private user-read-currently-playing user-read-playback-state'

AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize'
TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

# Create custom Flask to be able to use Vue syntax
class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    variable_start_string='%%',
    variable_end_string='%%',
  ))

app = CustomFlask(__name__)

# Auth endpoint
@app.route('/')
def index():
  authenticationUrl = (AUTH_ENDPOINT +
  '?response_type=code&client_id=' + SPOTIFY_CLIENT_ID +
  '&scope=' + quote(SCOPES) +
  '&redirect_uri=' + quote(REDIRECT_URI))
  
  return redirect(authenticationUrl)

# Callback endpoint
@app.route('/callback')
def callback():
  payload = {
    'grant_type': 'authorization_code',
    'client_id': SPOTIFY_CLIENT_ID,
    'client_secret': SPOTIFY_CLIENT_SECRET,
    'code': str(request.args['code']),
    'redirect_uri': REDIRECT_URI,
  }

  # Obtain access and refresh tokens
  SPOTIFY_ACCESS_TOKEN = requests.post(TOKEN_ENDPOINT, payload).json()['access_token']
  
  # REFRESH_TOKEN = res['refresh_token']
  # EXPIRES_IN = res['expires_in']
  
  global spotifyOptions, geniusOptions
  spotifyOptions = { 'Authorization' : 'Bearer ' + SPOTIFY_ACCESS_TOKEN }
  geniusOptions = { 'Authorization' : 'Bearer ' + GENIUS_ACCESS_TOKEN }

  return redirect('/home')

@app.route('/home')
def home():
  return render_template('index.html')

@app.route('/track', methods=['GET', 'POST'])
def track():
  songDetails = getSongInformation(spotifyOptions, geniusOptions)
  return jsonify(songDetails)

if __name__ == "__main__":
  app.run(port=3000)
