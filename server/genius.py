import requests
import re
from bs4 import BeautifulSoup

GENIUS_URL = 'https://api.genius.com'
# INPUT YOUR ACCESS TOKEN HERE
ACCESS_TOKEN = ''
headers = { 'Authorization' : 'Bearer ' + ACCESS_TOKEN }

def normalize(str):
    # remove remix from song name
    if "remix" in str.lower():
        try:
            str = str[:str.rindex('-')] # e.g. - [artist] remix
        except:
            try:
                str = str[:str.rindex('(')] # e.g. (remix)
            except:
                raise Exception('FAILED to normalize' + str + '!')

    # keep only alphanumeric characters and remove feat/with features from song name
    str = re.sub(r'\(.*\)', '', str)
    str = re.sub(r'[^A-Za-z0-9]+', '', str).lower()
    return str

def getLyrics(rawName, rawArtist):
    # 1. Normalize song and artist names
    try:
        name = normalize(rawName)
        artist = normalize(rawArtist)
    except Exception as e:
        raise e
    
    # 2. Get the Genius artist ID using artist name
    searchParams = {
        'q': artist
    }
    try:
        res = (requests.get(GENIUS_URL + '/search/' , params=searchParams, headers=headers)).json()
    except:
        raise Exception('FAILED to search Spotify for artist' + artist + '!')

    artistId = ''
    for hit in res['response']['hits']:
        try:
            artistNorm = normalize(hit['result']['primary_artist']['name'])
        except Exception as e:
            raise e

        if hit['type'] == 'song' and artistNorm == artist:
            artistId = hit['result']['primary_artist']['id']
            break
    
    # 3. Get the top 50 songs on Genius by artist ID
    songParams = {
        'id' : artistId,
        'per_page' : '50',
        'sort' : 'popularity'
    }
    try:
        res = (requests.get(GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=songParams, headers=headers)).json()
    except:
        raise Exception('FAILED to search artist songs!')

    # 4. Get the correct Genius song url for the song name
    songUrl = ''
    for song in res['response']['songs']:
        try:
            titleNorm = normalize(song['title'])
        except Exception as e:
            raise e

        if titleNorm == name:
            songUrl = song['url']
            break

    if not songUrl:
        raise Exception('FAILED to find song for artist' + artist + '!')

    # 5. Fetch and parse Genius html from song url
    try:
        page = requests.get(songUrl)
        html = BeautifulSoup(page.text, "html.parser")
    except:
        raise Exception('FAILED to load and parse Genuis song url!')
    
    # 6. Return song lyrics
    try:
        return html.find("div", class_="lyrics").get_text()
    except:
        raise Exception('FAILED to parse lyrics from html!')
