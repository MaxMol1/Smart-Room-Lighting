import requests

class GeniusController:
    def __init__(self):
        self.GENIUS_URL = 'https://api.genius.com'

    # Returns artist id using artist name
    def getGeniusSearchRes(self, params, headers):
        try:
            res = requests.get(self.GENIUS_URL + '/search/' , params=params, headers=headers)
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
            raise Exception('FAILED to retrieve Genius search results for: ' + params['q'])

    # Returns an artists top songs
    def getGeniusArtistSongs(self, artistId, params, headers):
        try:
            res = requests.get(self.GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=params, headers=headers)
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
            raise Exception('FAILED to retrieve artist songs by artistId: ' + str(artistId))

    # Returns web response from a Genius song url
    def getGeniusSongUrlRes(self, url):
        try:
            res = requests.get(url)
            res.raise_for_status()
            return res
        except requests.exceptions.HTTPError:
            raise
        except requests.exceptions.ConnectionError:
            raise
        except requests.exceptions.Timeout:
            raise
        except requests.exceptions.RequestException:
            raise
        except:
            raise Exception('FAILED to retrieve results from: ' + url)
