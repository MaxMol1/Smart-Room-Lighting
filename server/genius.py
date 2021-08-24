import requests
import json
import re
from bs4 import BeautifulSoup

GENIUS_URL = 'https://api.genius.com'
# INPUT ACCESS TOKEN HERE
ACCESS_TOKEN = ''
headers = { 'Authorization' : 'Bearer ' + ACCESS_TOKEN }

def normalize(str):
    # remove remix from song name
    if "remix" in str or "Remix" in str or "REMIX" in str:
        try:
            # e.g. - [artist] remix
            str = str[:str.rindex('-')]
        except:
            try:
                # e.g. (remix)
                str = str[:str.rindex('(')]
            except:
                print('Inconsistent naming convention!')
    # keep only alphanumeric characters and remove feat/with features from song name
    str = re.sub(r'\(.*\)', '', str)
    str = re.sub(r'[^A-Za-z0-9]+', '', str).lower()
    return str

def getLyrics(name, artist):
    name = normalize(name)
    artist = normalize(artist)
    
    # 1. Get artist ID using artist name
    searchParams = { 'q': artist }
    res = (requests.get(GENIUS_URL + '/search/' , params=searchParams, headers=headers)).json()

    artistId = ''
    for hit in res['response']['hits']:
        if hit['type'] == 'song' and normalize(hit['result']['primary_artist']['name']) == artist:
            artistId = hit['result']['primary_artist']['id']
            break
    
    # 2. Get top 50 songs by artist
    songParams = { 'id' : artistId, 'per_page' : '50', 'sort' : 'popularity' }
    res = (requests.get(GENIUS_URL + '/artists/' + str(artistId) + '/songs/', params=songParams, headers=headers)).json()

    # 3. Get correct song url from list of 50 songs
    songUrl = ''
    for song in res['response']['songs']:
        if normalize(song['title']) == name:
            songUrl = song['url']
            break

    # song not found
    if not songUrl:
        raise Exception('Song not found for artist:' + artist)

    # 4. Fetch and parse html from song url
    page = requests.get(songUrl)
    html = BeautifulSoup(page.text, "html.parser")
    
    # 5. Return lyrics
    try:
        return html.find("div", class_="lyrics").get_text()
    except:
        return ''
