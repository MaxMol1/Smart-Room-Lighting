from flask import Flask, request, redirect, render_template, jsonify
import requests
from urllib.parse import quote
from spotify import trackCurrentSong
from genius import getLyrics

# INPUT CLIENT ID HERE
CLIENT_ID = ''
# INPUT CLIENT SECRET HERE
CLIENT_SECRET = ''
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
  '?response_type=code&client_id=' + CLIENT_ID +
  '&scope=' + quote(SCOPES) +
  '&redirect_uri=' + quote(REDIRECT_URI))
  
  return redirect(authenticationUrl)

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
  songData = trackCurrentSong(options)

  if songData == {}:
    print ('No song playing, or song not found ...')
    return jsonify({'name' : '', 'artist' : '', 'date' : '', 'pop' : '', 'lyrics' : '', 'cover' : ''})

  songData['lyrics'] = getLyrics(songData['name'], songData['artists'][0]['name'])

  if songData['lyrics'] == '':
    print ('Lyrics not found ...')
    songData['lyrics'] = 'Could not fetch lyrics'

  return jsonify({'name' : songData['name'], 'artist' : songData['artists'][0]['name'],
    'date' : songData['date'], 'pop' : songData['pop'], 'lyrics' : songData['lyrics'],
    'cover' : songData['cover']})

if __name__ == "__main__":
  app.run(port=3000)
