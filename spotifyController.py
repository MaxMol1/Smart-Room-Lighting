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
            res = requests.post(self.TOKEN_ENDPOINT, data=data)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.Timeout:
            raise
        except requests.exceptions.RequestException:
            raise
        except:
            raise Exception('FAILED to generate Spotify access and refresh tokens')

    # Returns currently playing song and info
    def trackCurrentSong(self, headers):
        try:
            res = requests.get(self.CURRENTLY_PLAYING_ENDPOINT, headers=headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.Timeout:
            raise
        except requests.exceptions.RequestException:
            raise
        except:
            raise Exception('FAILED to retrieve currently playing song')


    # Returns genre of current playing song
    def trackCurrentSongGenres(self, artistId, headers):
        try:
            res = requests.get(self.ARTIST_ENDPOINT + str(artistId), headers=headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.Timeout:
            raise
        except requests.exceptions.RequestException:
            raise
        except:
            raise Exception('FAILED to retrieve genres for artistId: ' + str(artistId))
