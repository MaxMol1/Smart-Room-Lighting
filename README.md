# Smart-Room-Lighting

### Introduction

This is a project that uses localhost to show information in real time about the current song playing on Spotify. This includes the full song name, artist, release date, genre, and full lyrics. It also includes both an emotion and sentiment analyzer for the lyrics that work together to map colors to match the mood of the song.

This project will support communication over WiFi with an ESP8266 microcontroller for the purpose of broadcasting the colors of the current song to an LED strip. Currently, the colors are only displayed on a web page along with the other information.

### Setting Up

To begin, you need to create an API client using [Genius](https://genius.com/developers). Pick an app name and a website, and then generate an access token when you see your client id and client secret. Paste the access token in line 22 of **songService.py**

You also need to create a developer account with [Spotify](https://developer.spotify.com/dashboard/login). Create a new application and be sure to 
1. Take your client id and client secret and paste these in line 14 and 15 of **songService.py**
2. Set the redirect uri of the app to be **http://127.0.0.1:3000/callback**

Before you begin, install all Python dependencies from the base directory

```pip install -r requirements.txt```

Launch the local server from the root directory using: **python3 server.py** and navigate to http://127.0.0.1:3000 in your browser of choice. Log in with your Spotify account to use the application. Click the button **Track** to see live results of the current song that you have playing.
