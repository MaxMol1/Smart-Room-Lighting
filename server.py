from flask import Flask, request, session, redirect, render_template, jsonify
import requests
import secrets
from urllib.parse import quote
from service import SongService

# INPUT YOUR SPOTIFY CLIENT ID AND CLIENT SECRET HERE
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
# INPUT YOUR GENIUS ACCESS TOKEN HERE
GENIUS_ACCESS_TOKEN = ''
SPOTIFY_AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
SPOTIFY_SCOPES = 'user-read-private user-read-currently-playing user-read-playback-state'
REDIRECT_URI = 'http://127.0.0.1:3000/callback'

# Create custom Flask to be able to use Vue syntax
class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    variable_start_string='%%',
    variable_end_string='%%',
  ))

app = CustomFlask(__name__)
app.secret_key = secrets.token_urlsafe(16)

songService = SongService()

# Auth endpoint
@app.route('/')
def index():
  authUrl = (SPOTIFY_AUTH_ENDPOINT +
  '?response_type=code&client_id=' + SPOTIFY_CLIENT_ID +
  '&scope=' + quote(SPOTIFY_SCOPES) +
  '&redirect_uri=' + quote(REDIRECT_URI))
  
  return redirect(authUrl)

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
  SPOTIFY_ACCESS_TOKEN = requests.post(SPOTIFY_TOKEN_ENDPOINT, payload).json()['access_token']
  # REFRESH_TOKEN = res['refresh_token']
  # EXPIRES_IN = res['expires_in']
  
  session['spotifyHeaders'] = { 'Authorization' : 'Bearer ' + SPOTIFY_ACCESS_TOKEN }
  session['geniusHeaders'] = { 'Authorization' : 'Bearer ' + GENIUS_ACCESS_TOKEN }

  return redirect('/home')

# Application home
@app.route('/home')
def home():
  return render_template('index.html')

# Tracking endpoint
@app.route('/track', methods=['GET', 'POST'])
def track():
  songDetails = songService.getSongInformation(spotifyHeaders=session.get('spotifyHeaders', None), geniusHeaders=session.get('geniusHeaders', None))
  return jsonify(songDetails)

if __name__ == "__main__":
  app.run(port=3000)
