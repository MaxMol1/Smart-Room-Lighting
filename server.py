from flask import Flask, request, session, redirect, render_template, jsonify
import secrets
from songService import SongService

# Create custom Flask to be able to use Vue syntax
class CustomFlask(Flask):
  jinja_options = Flask.jinja_options.copy()
  jinja_options.update(dict(
    variable_start_string='%%',
    variable_end_string='%%',
  ))

# Create app and song service
app = CustomFlask(__name__)
app.secret_key = secrets.token_urlsafe(16)
songService = SongService()

# Entry endpoint
@app.route('/')
def index():
  if not session.get('SPOTIFY_ACCESS_TOKEN', None):
    return redirect(songService.authenticateSpotifyUser())
  else:
    return render_template('index.html')

# Callback auth endpoint
@app.route('/callback')
def callback():
  res = songService.generateSpotifyTokens(code=str(request.args['code']))
  session['SPOTIFY_ACCESS_TOKEN'] = res['access_token']
  session['SPOTIFY_REFRESH_TOKEN'] = res['refresh_token']
  session['GENIUS_ACCESS_TOKEN'] = ''
  return redirect('/')

# Tracking endpoint
@app.route('/track', methods=['GET'])
def track():
  if not session.get('SPOTIFY_ACCESS_TOKEN', None):
    return redirect('/')
  try:
    return jsonify(songService.getSongInformation(
      spotifyHeaders={ 'Authorization': 'Bearer ' + session.get('SPOTIFY_ACCESS_TOKEN', None) },
      geniusHeaders={ 'Authorization': 'Bearer ' + session.get('GENIUS_ACCESS_TOKEN', None) }
    ))
  except:
    res = songService.reGenerateSpotifyTokens(refresh_token=session['SPOTIFY_REFRESH_TOKEN'])
    session['SPOTIFY_ACCESS_TOKEN'] = res['access_token']
    return redirect('/track')

if __name__ == "__main__":
  app.run(port=3000)
