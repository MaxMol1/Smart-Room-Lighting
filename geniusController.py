import requests

GENIUS_URL = 'https://api.genius.com'

# Returns artist id using artist name
def getGeniusArtistId(params, headers):
    res = requests.get(GENIUS_URL + '/search/' , params=params, headers=headers)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception('FAILED to search Genius by artist name: ' + params['q'])

    return res.json()

# Returns an artists top songs
def getArtistTopSongs(artistId, params, headers):
    res = requests.get(GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=params, headers=headers)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception('FAILED to search Genius by artistId: ' + artistId)

    return res.json()

# Returns web response from a Genius song url
def getGeniusSongUrlRes(url):
    res = requests.get(url)

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception('FAILED to search Genuis by song url: ' + url)

    return res
