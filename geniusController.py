import requests

GENIUS_URL = 'https://api.genius.com'

# Returns artist id using artist name
def getGeniusArtistId(params, headers):
    try:
        return requests.get(GENIUS_URL + '/search/' , params=params, headers=headers).json()
    except:
        raise Exception('FAILED to search Genius by artist name: ' + params['q'])

# Returns an artists top songs
def getArtistTopSongs(artistId, params, headers):
    try:
        return requests.get(GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=params, headers=headers).json()
    except:
        raise Exception('FAILED to search Genius by artistId: ' + artistId)

# Returns web response from a Genius song url
def getGeniusSongUrlRes(url):
    try:
        return requests.get(url)
    except:
        raise Exception('FAILED to search Genuis by song url: ' + url)
