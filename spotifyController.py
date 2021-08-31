import requests
from requests.models import HTTPError

class SpotifyController:
    def __init__(self):
        self.AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize'
        self.TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
        self.CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'
        self.ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/'

    # Returns correct endpoint for authentication
    def authRedirect(self, url):
        return self.AUTH_ENDPOINT + url

    # Returns response from token endpoint
    def generateTokens(self, data):
        try:
            return requests.post(self.TOKEN_ENDPOINT, data=data).json()
        except:
            raise Exception('FAILED to generate Spotify access and refresh tokens')

    # Returns currently playing song and info
    def trackCurrentSong(self, headers):
        try:
            res = requests.get(self.CURRENTLY_PLAYING_ENDPOINT, headers=headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError as e:
            raise
        except:
            raise Exception('FAILED to track current playing song')


    # Returns genre of current playing song
    def trackCurrentSongGenres(self, artistId, headers):
        try:
            return requests.get(self.ARTIST_ENDPOINT + str(artistId), headers=headers).json()
        except:
            raise Exception('FAILED to fetch artist genres for artistId: ' + str(artistId))
