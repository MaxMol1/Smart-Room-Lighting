import requests

CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'
ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/'

# Returns currently playing song and info
def trackCurrentSong(headers):
    try:
        return requests.get(CURRENTLY_PLAYING_ENDPOINT, headers=headers).json()
    except:
        raise Exception('FAILED to track current playing song')

# Returns genre of current playing song
def trackCurrentSongGenres(artistId, headers):
    try:
        return requests.get(ARTIST_ENDPOINT + str(artistId), headers=headers).json()
    except:
        raise Exception('FAILED to fetch artist genres for artistId: ' + str(artistId))
