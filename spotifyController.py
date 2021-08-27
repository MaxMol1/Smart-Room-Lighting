import requests

CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'
ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/'

# Returns currently playing song and info
def trackCurrentSong(spotifyOptions):
    try:
        return requests.get(CURRENTLY_PLAYING_ENDPOINT, headers=spotifyOptions).json()
    except:
        raise Exception('FAILED to track current playing song')

# Returns genre of current playing song
def trackCurrentSongGenres(artistId, spotifyOptions):
    try:
        return requests.get(ARTIST_ENDPOINT + artistId, headers=spotifyOptions).json()
    except:
        raise Exception('FAILED to fetch artist genres for artistId: ' + artistId)
