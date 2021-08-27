import re
from bs4 import BeautifulSoup
from spotifyController import trackCurrentSong, trackCurrentSongGenres
from geniusController import getGeniusArtistId, getArtistTopSongs, getGeniusSongUrlRes
from models.emotionModel import getSongEmotion
from models.sentimentModel import getSongSentiment

def normalize(str):
    # remove remix from song name
    if "remix" in str.lower():
        try:
            str = str[:str.rindex('-')] # e.g. - [artist] remix
        except:
            try:
                str = str[:str.rindex('(')] # e.g. (remix)
            except:
                raise Exception('FAILED to normalize' + str)

    # keep only alphanumeric characters and remove feat/with features from song name
    str = re.sub(r'\(.*\)', '', str)
    str = re.sub(r'[^A-Za-z0-9]+', '', str).lower()
    return str

# Service method to fetch all song details
def getSongInformation(spotifyOptions, geniusOptions):
    # Object to store all song details
    songDetails = {
        'name': '',
        'date': '',
        'artist': '',
        'artistId': '',
        'cover': '',
        'pop': '',
        'genres': [],
        'lyrics': '',
        'emotions': (),
        'sentiment': '',
        'colors': ()
    }

    # Fetch general information
    try:
        songRes = trackCurrentSong(spotifyOptions)
        songDetails['name'] = songRes['item']['name']
        songDetails['date'] = songRes['item']['album']['release_date']
        songDetails['artist'] = songRes['item']['artists'][0]['name']
        songDetails['artistId'] = songRes['item']['artists'][0]['id']
        songDetails['cover'] = songRes['item']['album']['images'][0]['url']
        songDetails['pop'] = songRes['item']['popularity']
    except Exception as e:
        print (e)
        return

    # Fetch song genres
    try:
        genresRes = trackCurrentSongGenres(songDetails['artistId'], spotifyOptions)
        songDetails['genres'] = genresRes['genres']
    except Exception as e:
        print (e)

    # Fetch song lyrics
    try:
        # Normalize song and artist names
        songNameNorm = normalize(songDetails['name'])
        artistNameNorm = normalize(songDetails['artist'])
        
        # Get the Genius artist ID using artist name
        res = getGeniusArtistId(params={'q': artistNameNorm}, geniusOptions=geniusOptions)
        artistId = ''
        for hit in res['response']['hits']:
            artistNorm = normalize(hit['result']['primary_artist']['name'])
            if hit['type'] == 'song' and artistNorm == artistNameNorm:
                artistId = hit['result']['primary_artist']['id']
                break
        
        # Get the correct Genius song url for the song name
        res = getArtistTopSongs(artistId=artistId, params={'id' : artistId, 'per_page' : '50', 'sort' : 'popularity'}, geniusOptions=geniusOptions)
        songUrl = ''
        for song in res['response']['songs']:
            titleNorm = normalize(song['title'])

            if titleNorm == songNameNorm:
                songUrl = song['url']
                break

        if not songUrl:
            raise Exception('FAILED to find current playing song for artist on Genius')

        # Fetch and parse Genius html from song url
        res = getGeniusSongUrlRes(songUrl=songUrl)
        html = BeautifulSoup(res.text, "html.parser")
        delimiter = '**'
        for br in html.findAll('br'):
            br.replaceWith(delimiter)
        for lyricsContainer in html.select('div[class*="Lyrics__Container-"]'):
            lyricsSegment = lyricsContainer.get_text().split(delimiter)
            songDetails['lyrics'] += "\n".join(line for line in lyricsSegment)

    except Exception as e:
        print (e)

    try:
        songDetails['emotions'] = getSongEmotion(songDetails['lyrics'])
        songDetails['sentiment'] = getSongSentiment(songDetails['lyrics'])
        customColorMapping = {
            ('P', 'Happy'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            {'P', 'Angry'}: ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            {'P', 'Surprise'}: ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('P', 'Sad'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('P', 'Fear'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('N', 'Happy'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('N', 'Angry'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('N', 'Surprise'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('N', 'Sad'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('N', 'Fear'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('NU', 'Happy'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('NU', 'Angry'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('NU', 'Surprise'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('NU', 'Sad'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
            ('NU', 'Fear'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 255, 'b': 128}),
        }
        songDetails['colors'] = customColorMapping[(songDetails['sentiment'], songDetails['emotions'][0])]

    except Exception as e:
        print (e)

    return songDetails
