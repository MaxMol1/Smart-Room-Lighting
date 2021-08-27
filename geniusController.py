import requests

GENIUS_URL = 'https://api.genius.com'

# Returns artist id using artist name
def getGeniusArtistId(params, geniusOptions):
    try:
        return requests.get(GENIUS_URL + '/search/' , params=params, headers=geniusOptions).json()
    except:
        raise Exception('FAILED to search Genius for artist by name: ' + params['q'])

# Returns an artists top songs
def getArtistTopSongs(artistId, params, geniusOptions):
    try:
        return requests.get(GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=params, headers=geniusOptions).json()
    except:
        raise Exception('FAILED to search Genius songs for artistId: ' + artistId)

# Returns web response from a Genius song url
def getGeniusSongUrlRes(songUrl):
    try:
        return requests.get(songUrl)
    except:
        raise Exception('FAILED to load and parse Genuis url: ' + songUrl)
