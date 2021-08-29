import requests

class SpotifyController:
    def __init__(self):
        self.CURRENTLY_PLAYING_ENDPOINT = 'https://api.spotify.com/v1/me/player/currently-playing'
        self.ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/'

    # Returns currently playing song and info
    def trackCurrentSong(self, headers):
        try:
            return requests.get(self.CURRENTLY_PLAYING_ENDPOINT, headers=headers).json()
        except:
            raise Exception('FAILED to track current playing song')

    # Returns genre of current playing song
    def trackCurrentSongGenres(self, artistId, headers):
        try:
            return requests.get(self.ARTIST_ENDPOINT + str(artistId), headers=headers).json()
        except:
            raise Exception('FAILED to fetch artist genres for artistId: ' + str(artistId))
