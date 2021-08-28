import requests

CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'
ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/'

# Returns currently playing song and info
def trackCurrentSong(headers):
    res = requests.get(CURRENTLY_PLAYING_ENDPOINT, headers=headers)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception('FAILED to track current playing song')

    return res.json()

# Returns genre of current playing song
def trackCurrentSongGenres(artistId, headers):
    res = requests.get(ARTIST_ENDPOINT + artistId, headers=headers)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception('FAILED to fetch artist genres for artistId: ' + artistId)

    return res.json()
