import requests
import json

CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'

# Returns dict after tracking song information
def track_current_song(options):
    song_data = {}
    res = (requests.get(CURRENTLY_PLAYING_ENDPOINT, headers=options)).json()

    song_data['name'] = res['item']['name']
    song_data['artists'] = res['item']['artists']
    song_data['date'] = res['item']['album']['release_date']
    # genre
    song_data['pop'] = res['item']['popularity']

    return song_data
