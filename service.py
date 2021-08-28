import re
import string
import datetime
from bs4 import BeautifulSoup
from spotifyController import trackCurrentSong, trackCurrentSongGenres
from geniusController import getGeniusArtistId, getArtistTopSongs, getGeniusSongUrlRes
from models.emotionModel import getSongEmotion
from models.sentimentModel import getSongSentiment

global songCache
songCache = {
    'name': '',
    'artist': ''
}

# Normalize artist names
def normalizeArtist(artist):
    artist = (artist.encode('ascii', 'ignore')).decode("utf-8")
    return artist.replace(' ', '-').lower().strip()

# Normalize sone names
def normalizeSong(name):
    name = (name.encode('ascii', 'ignore')).decode("utf-8")
    
    # remove remix from song name
    if "remix" in name.lower():
        try:
            name = name[:name.rindex('-')] # e.g. - [artist] remix
        except:
            try:
                name = name[:name.rindex('(')] # e.g. (remix)
            except:
                try:
                    name = name[:name.rindex('REMIX')] # e.g. REMIX
                except:
                    raise Exception('FAILED to normalize ' + name)

    # keep only alphanumeric characters and remove feat/with features from song name
    name = re.sub(r'\(.*\)', '', name)
    name = re.sub(r'[^A-Za-z0-9]+', '', name).lower()
    return name

# Service method to fetch all song details
def getSongInformation(spotifyOptions, geniusOptions):
    # Object to store all song details
    songDetails = {
        'name': '',
        'artist': '',
        'date': '',
        'spotifyArtistId': 0,
        'cover': '',
        'pop': 0,
        'genres': [],
        'lyrics': '',
        'emotions': (),
        'sentiment': '',
        'colors': ({'r' : 236, 'g' : 240, 'b' : 241}, {'r' : 236, 'g' : 240, 'b' : 241})
    }

    # Fetch general information
    try:
        res = trackCurrentSong(headers=spotifyOptions)
        songDetails['name'] = res['item']['name']
        songDetails['artist'] = res['item']['artists'][0]['name']

        # Same song is playing
        if songCache['name'] == songDetails['name'] and songCache['artist'] == songDetails['artist']:
            return {}

        try:
            songDetails['date'] = datetime.datetime.strptime(res['item']['album']['release_date'], "%Y-%m-%d").date().strftime("%B %d, %Y")
        except:
            songDetails['date'] = res['item']['album']['release_date']
        songDetails['spotifyArtistId'] = res['item']['artists'][0]['id']
        songDetails['cover'] = res['item']['album']['images'][0]['url']
        songDetails['pop'] = res['item']['popularity']

        # set song cache
        songCache['name'] = songDetails['name']
        songCache['artist'] = songDetails['artist']
    except Exception as e:
        print (e)
        return

    # Fetch song genres
    try:
        res = trackCurrentSongGenres(artistId=songDetails['spotifyArtistId'], headers=spotifyOptions)
        songDetails['genres'] = [string.capwords(x) for x in res['genres']]
        if songDetails['genres'] == []:
            print ('... WARNING: no genres found for ' + songDetails['artist'])
    except Exception as e:
        print (e)

    # Fetch song lyrics
    try:
        # Normalize and artist and song names
        artistNameNorm = normalizeArtist(songDetails['artist'])
        songNameNorm = normalizeSong(songDetails['name'])
        
        # Get the Genius artist ID using artist name
        res = getGeniusArtistId(params={'q': artistNameNorm}, headers=geniusOptions)
        geniusArtistId = 0
        for hit in res['response']['hits']:
            artistNorm = normalizeArtist(hit['result']['primary_artist']['name'])
            if hit['type'] == 'song' and artistNorm == artistNameNorm:
                geniusArtistId = hit['result']['primary_artist']['id']
                break
        
        if geniusArtistId == 0:
            raise Exception('FAILED to find ' + songDetails['artist'] + ' on Genius')

        print ('... found Genius artistId: ' + str(geniusArtistId) + ' for artist ' + songDetails['artist'])

        # Get the correct Genius song url for the song name
        songUrl = ''
        pageIndex = 1
        while True:
            print ('... searching results for ' + songDetails['name'] + ' on page ' + str(pageIndex))
            res = getArtistTopSongs(artistId=geniusArtistId, params={'id': str(geniusArtistId), 'per_page': '50', 'sort': 'popularity', 'page': pageIndex}, headers=geniusOptions)
            for song in res['response']['songs']:
                titleNorm = normalizeSong(song['title'])
                if titleNorm == songNameNorm:
                    songUrl = song['url']
                    break
            else:
                if not res['response']['next_page']:
                    break
                else:
                    pageIndex += 1
                    continue
            break

        if not songUrl:
            raise Exception('FAILED to find ' + songDetails['name'] + ' for ' + songDetails['artist'] + ' on Genius')

        print ('... found song url: ' + songUrl)

        # Fetch and parse Genius html from song url
        res = getGeniusSongUrlRes(url=songUrl)
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

        print ('... identified song as ' + songDetails['emotions'][0] + ' ' + songDetails['sentiment'])

        customColorMapping = {
            ('Positive', 'Happy'): ({'r': 255, 'g': 255, 'b': 50}, {'r': 255, 'g': 153, 'b': 102}),
            ('Positive', 'Angry'): ({'r': 255, 'g': 255, 'b': 102}, {'r': 255, 'g': 128, 'b': 128}),
            ('Positive', 'Surprise'): ({'r': 255, 'g': 204, 'b': 102}, {'r': 153, 'g': 255, 'b': 153}),
            ('Positive', 'Sad'): ({'r': 255, 'g': 255, 'b': 102}, {'r': 128, 'g': 170, 'b': 255}),
            ('Positive', 'Fear'): ({'r': 255, 'g': 255, 'b': 128}, {'r': 255, 'g': 153, 'b': 187}),

            ('Negative', 'Happy'): ({'r': 0, 'g': 153, 'b': 230}, {'r': 221, 'g': 153, 'b': 225}),
            ('Negative', 'Angry'): ({'r': 255, 'g': 51, 'b': 51}, {'r': 51, 'g': 26, 'b': 0}),
            ('Negative', 'Surprise'): ({'r': 255, 'g': 230, 'b': 179}, {'r': 128, 'g': 255, 'b': 234}),
            ('Negative', 'Sad'): ({'r': 255, 'g': 179, 'b': 179}, {'r': 179, 'g': 242, 'b': 255}),
            ('Negative', 'Fear'): ({'r': 0, 'g': 179, 'b': 149}, {'r': 170, 'g': 0, 'b': 204}),

            ('Neutral', 'Happy'): ({'r': 255, 'g': 212, 'b': 128}, {'r': 153, 'g': 221, 'b': 255}),
            ('Neutral', 'Angry'): ({'r': 234, 'g': 128, 'b': 255}, {'r': 255, 'g': 102, 'b': 102}),
            ('Neutral', 'Surprise'): ({'r': 128, 'g': 255, 'b': 149}, {'r': 213, 'g': 204, 'b': 255}),
            ('Neutral', 'Sad'): ({'r': 255, 'g': 128, 'b': 255}, {'r': 153, 'g': 238, 'b': 255}),
            ('Neutral', 'Fear'): ({'r': 255, 'g': 153, 'b': 102}, {'r': 255, 'g': 230, 'b': 238}),
        }
        songDetails['colors'] = customColorMapping[(songDetails['sentiment'], songDetails['emotions'][0])]

    except Exception as e:
        print (e)

    return songDetails
