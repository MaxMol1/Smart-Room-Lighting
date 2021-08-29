from flask import Flask, request, redirect, render_template, jsonify
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
songService = SongService()

# Entry endpoint
@app.route('/')
def index():
  if not songService.isSpotifyUserAuthenticated():
    return redirect(songService.authenticateSpotifyUser())
  else:
    return render_template('index.html')

# Callback auth endpoint
@app.route('/callback')
def callback():
  songService.generateSpotifyTokens(str(request.args['code']))
  return redirect('/')

# Tracking endpoint
@app.route('/track', methods=['GET'])
def track():
  songDetails = songService.getSongInformation()
  return jsonify(songDetails)

if __name__ == "__main__":
  app.run(port=3000)
