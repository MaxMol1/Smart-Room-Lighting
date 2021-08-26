import requests

CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'

# Returns currently playing song and info
def trackCurrentSong(options):
    try:
        res = (requests.get(CURRENTLY_PLAYING_ENDPOINT, headers=options)).json()
    except:
        raise Exception('FAILED to track current playing song!')

    return {
        'name': res['item']['name'],
        'artists': res['item']['artists'],
        'date': res['item']['album']['release_date'],
        'cover': res['item']['album']['images'][0]['url'],
        'pop': res['item']['popularity']
    }
