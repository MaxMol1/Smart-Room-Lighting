import requests

class GeniusController:
    def __init__(self):
        self.GENIUS_URL = 'https://api.genius.com'

    # Returns artist id using artist name
    def getGeniusArtistId(self, params, headers):
        try:
            return requests.get(self.GENIUS_URL + '/search/' , params=params, headers=headers).json()
        except:
            raise Exception('FAILED to search Genius by artist name: ' + params['q'])

    # Returns an artists top songs
    def getArtistTopSongs(self, artistId, params, headers):
        try:
            return requests.get(self.GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=params, headers=headers).json()
        except:
            raise Exception('FAILED to search Genius by artistId: ' + str(artistId))

    # Returns web response from a Genius song url
    def getGeniusSongUrlRes(self, url):
        try:
            return requests.get(url)
        except:
            raise Exception('FAILED to search Genuis by song url: ' + url)
