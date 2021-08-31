from urllib.parse import quote
import os
import re
import string
import datetime
from bs4 import BeautifulSoup
from requests.models import HTTPError
from spotifyController import SpotifyController
from geniusController import GeniusController
from models.emotionModel import EmotionModel
from models.sentimentModel import SentimentModel

class SongService:
    def __init__(self):
        # INPUT YOUR SPOTIFY CLIENT ID AND CLIENT SECRET HERE
        self.SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
        self.SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
        self.SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:3000/callback'
        self.SPOTIFY_SCOPES = 'user-read-private user-read-currently-playing user-read-playback-state'

        self.spotifyController = SpotifyController()
        self.geniusController = GeniusController()
        self.emotionModel = EmotionModel()
        self.sentimentModel = SentimentModel()

        self.songCache = {
            'name': '',
            'artist': ''
        }

    # Authenticate Spotify user
    def authenticateSpotifyUser(self):
        url = ('?response_type=code&client_id=' + self.SPOTIFY_CLIENT_ID +
            '&scope=' + quote(self.SPOTIFY_SCOPES) +
            '&redirect_uri=' + quote(self.SPOTIFY_REDIRECT_URI))

        return self.spotifyController.authRedirect(url=url)

    # Generate access and refresh tokens for Spotify
    def generateSpotifyTokens(self, code):
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.SPOTIFY_CLIENT_ID,
            'client_secret': self.SPOTIFY_CLIENT_SECRET,
            'code': code,
            'redirect_uri': self.SPOTIFY_REDIRECT_URI,
        }

        try:
            return self.spotifyController.generateTokens(data=data)
        except Exception as e:
            print (e)
            return { 'access_token': '', 'refresh_token': '' }

    def reGenerateSpotifyTokens(self, refresh_token):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.SPOTIFY_CLIENT_ID,
            'client_secret': self.SPOTIFY_CLIENT_SECRET
        }

        try:
            return self.spotifyController.generateTokens(data=data)
        except Exception as e:
            print (e)
            return { 'access_token': '' }

    # Get general song info
    def getGeneralInfo(self, songDetails, spotifyHeaders):
        # Try to track current playing song
        res = self.spotifyController.trackCurrentSong(headers=spotifyHeaders)

        songDetails['name'] = res['item']['name']
        songDetails['artist'] = res['item']['artists'][0]['name']

        # Same song is playing
        if self.songCache['name'] == songDetails['name'] and self.songCache['artist'] == songDetails['artist']:
            raise Exception('FAILED to detect change in song')

        try:
            songDetails['date'] = datetime.datetime.strptime(res['item']['album']['release_date'], "%Y-%m-%d").date().strftime("%B %d, %Y")
        except:
            songDetails['date'] = res['item']['album']['release_date']
        songDetails['spotifyArtistId'] = res['item']['artists'][0]['id']
        songDetails['cover'] = res['item']['album']['images'][0]['url']
        songDetails['pop'] = res['item']['popularity']

        # set song cache
        self.songCache['name'] = songDetails['name']
        self.songCache['artist'] = songDetails['artist']

        # return songDetails
        return songDetails

    # Get song genres
    def getGenres(self, songDetails, spotifyHeaders):
        res = self.spotifyController.trackCurrentSongGenres(artistId=songDetails['spotifyArtistId'], headers=spotifyHeaders)

        songDetails['genres'] = [string.capwords(x) for x in res['genres']]
        if songDetails['genres'] == []:
            raise Exception('... WARNING: no genres found for ' + songDetails['artist'])

        return songDetails

    # Normalize sone names
    def normalizeSong(self, name):
        name = (name.encode('ascii', 'ignore')).decode("utf-8").lower()
        name = re.sub("[\(\[].*?[\)\]]", "", name)
        
        if ' - ' in name:
            name = name[:name.rindex(' - ')]
        if ' remix' in name:
            name = name[:name.rindex(' remix')]

        return name.strip()

    # Normalize artist names
    def normalizeArtist(self, artist):
        artist = (artist.encode('ascii', 'ignore')).decode("utf-8").lower()

        return artist.replace(' ', '-').strip()

    # Get song lyrics
    def getLyrics(self, songDetails, geniusHeaders):
        # Normalize and artist and song names
        songNameNorm = self.normalizeSong(songDetails['name'])
        artistNameNorm = self.normalizeArtist(songDetails['artist'])
        songUrl = ''
        geniusArtistId = 0

        # Search Genius using song name
        print ('... Searching Genius for ' + songDetails['name'] + ' by ' + songDetails['artist'])
        res = self.geniusController.getGeniusSearchRes(params={'q': songNameNorm + ' ' + artistNameNorm, 'per_page': 20}, headers=geniusHeaders)
        for hit in res['response']['hits']:
            songNorm = self.normalizeSong(hit['result']['title'])
            artistNorm = self.normalizeArtist(hit['result']['primary_artist']['name'])

            if hit['type'] == 'song' and artistNorm == artistNameNorm:
                geniusArtistId = hit['result']['primary_artist']['id']
                if songNorm == songNameNorm:
                    songUrl = hit['result']['url']
                    break

        # Search by song did not yield correct artist
        if not geniusArtistId:
            print ('... Search by song unsuccessful. Searching Genius for ' + songDetails['artist'])
            # Search Genius using artist name
            res = self.geniusController.getGeniusSearchRes(params={'q': artistNameNorm}, headers=geniusHeaders)
            for hit in res['response']['hits']:
                songNorm = self.normalizeSong(hit['result']['title'])
                artistNorm = self.normalizeArtist(hit['result']['primary_artist']['name'])

                if hit['type'] == 'song' and artistNorm == artistNameNorm:
                    geniusArtistId = hit['result']['primary_artist']['id']
                    if songNorm == songNameNorm:
                        songUrl = hit['result']['url']
                        break

            # Artist not found on Genius
            if geniusArtistId == 0:
                raise Exception('FAILED to find ' + songDetails['artist'] + ' on Genius')

            print ('... found Genius artistId: ' + str(geniusArtistId) + ' for artist ' + songDetails['artist'])

        # Search by song or artist did not yield a proper result
        if not songUrl:
            # Get the correct Genius song url for the song name
            pageIndex = 1
            while True:
                print ('... searching results for ' + songDetails['name'] + ' on page ' + str(pageIndex))
                res = self.geniusController.getGeniusArtistSongs(artistId=geniusArtistId, params={'id': str(geniusArtistId), 'per_page': '50', 'sort': 'popularity', 'page': pageIndex}, headers=geniusHeaders)
                for song in res['response']['songs']:
                    songNorm = self.normalizeSong(song['title'])
                    if songNorm == songNameNorm:
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
        res = self.geniusController.getGeniusSongUrlRes(url=songUrl)
        html = BeautifulSoup(res.text, "html.parser")
        delimiter = '**'
        for br in html.findAll('br'):
            br.replaceWith(delimiter)
        for lyricsContainer in html.select('div[class*="Lyrics__Container-"]'):
            lyricsSegment = lyricsContainer.get_text().split(delimiter)
            songDetails['lyrics'] += "\n".join(line for line in lyricsSegment)

        if songDetails['lyrics'] == '':
            songDetails['lyrics'] = 'This is an instrumental!'

        return songDetails

    # Get song emotions, sentiment, and colors
    def getColors(self, songDetails):
        # process lyrics
        parsedLyrics = re.sub("[\(\[].*?[\)\]]", "", songDetails['lyrics']).lower()
        parsedLyricsList = [line for line in parsedLyrics.split('\n') if line]

        # get emotion and sentiment
        songDetails['emotions'] = self.emotionModel.getSongEmotion(parsedLyrics)
        songDetails['sentiment'] = self.sentimentModel.getSongSentiment(parsedLyricsList)

        print ('... identified song as having ' + songDetails['emotions'][0] + ' emotion and ' + songDetails['sentiment'] + ' sentiment')

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

        return songDetails

    # Service method to fetch all song details
    def getSongInformation(self, spotifyHeaders, geniusHeaders):
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
            songDetails = self.getGeneralInfo(songDetails=songDetails, spotifyHeaders=spotifyHeaders)
        except HTTPError as e:
            print (e)
            raise
        except Exception as e:
            print (e)
            return {}

        # Fetch song genres
        try:
            songDetails = self.getGenres(songDetails=songDetails, spotifyHeaders=spotifyHeaders)
        except Exception as e:
            print (e)

        # Fetch song lyrics
        try:
            songDetails = self.getLyrics(songDetails=songDetails, geniusHeaders=geniusHeaders)
        except Exception as e:
            print (e)

        # Fetch song colors
        try:
            songDetails = self.getColors(songDetails=songDetails)
        except Exception as e:
            print (e)

        return songDetails
