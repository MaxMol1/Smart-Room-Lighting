import requests
import json
import re
from bs4 import BeautifulSoup

GENIUS_URL = 'https://api.genius.com'
# INPUT ACCESS TOKEN HERE
ACCESS_TOKEN = ''
headers = { 'Authorization' : 'Bearer ' + ACCESS_TOKEN }

def normalize(str):
    return re.sub(r'[^A-Za-z0-9]+', '', str).lower()

def get_lyrics(name, artist):
    name = normalize(name)
    artist = normalize(artist)
    
    # 1. Get artist ID using artist name
    search_params = { 'q': artist }
    res = (requests.get(GENIUS_URL + '/search/' , params=search_params, headers=headers)).json()

    artist_id = ''
    for hit in res['response']['hits']:
        if hit['type'] == 'song' and normalize(hit['result']['primary_artist']['name']) == artist:
            artist_id = hit['result']['primary_artist']['id']
            break
    
    # 2. Get top 50 songs by artist
    song_params = { 'id' : artist_id, 'per_page' : '50', 'sort' : 'popularity' }
    res = (requests.get(GENIUS_URL + '/artists/' + str(artist_id) + '/songs/', params=song_params, headers=headers)).json()

    # 3. Get correct song url from list of 50 songs
    song_url = ''
    for song in res['response']['songs']:
        if normalize(song['title']) == name:
            song_url = song['url']
            break

    # song not found
    if not song_url:
        raise Exception('Song not found for artist:' + artist)

    # 4. Fetch and parse html from song url
    page = requests.get(song_url)
    html = BeautifulSoup(page.text, "html.parser")
    
    # 5. Return lyrics
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics
