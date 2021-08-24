import requests

CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'

# Returns dictionary after tracking song information
def trackCurrentSong(options):
    songData = {}
    res = {}

    try:
        res = (requests.get(CURRENTLY_PLAYING_ENDPOINT, headers=options)).json()
    except:
        return {}

    songData['name'] = res['item']['name']
    songData['artists'] = res['item']['artists']
    songData['date'] = res['item']['album']['release_date']
    songData['cover'] = res['item']['album']['images'][0]['url']
    # genre
    songData['pop'] = res['item']['popularity']

    return songData
