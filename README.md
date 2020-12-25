# Sound-Reactive-LED

### Introduction

This is a project that uses localhost to show information in real time about songs that a Spotify user plays including the lyrics, genres, release date, and mood. It also includes a sentiment analyzer that maps colors to a song based on the sentiment of its lyrics.

This project supports communication over WiFi with an ESP8266 microcontroller for the purpose of broadcasting the colors of the current song to lights and LED strips to match the mood.

### Setting Up

To begin, you need to create an API client using [Genius](https://genius.com/developers). Pick an app name and a website, and then generate an access token when you see your client id and client secret. Paste the access token in line 8 of **server/genius.py**

You also need to create a developer account with [Spotify](https://developer.spotify.com/dashboard/login). Create a new application and be sure to 
1. Take your client id and client secret and paste these in line 9 and 11 of **server/server.py**
2. Set the redirect uri of the app to be **http://127.0.0.1:3000/callback**

Before you begin, install all Python dependencies from the base directory

```pip install -r requirements.txt```

Launch the local server using: **python3 server.py** and navigate to http://127.0.0.1:3000 in your browser of choice. Log in with your Spotify account to use the application. Click the button **Start Tracking** to see live results of the current song that you have playing.

### Classifying Song

Navigate to the models directory and run **python3 model.py** with the arguments for song name and artist to classify a song as positive, negative, or mellow.

**Note:** Make sure to enter the song name and artist exactly and surrounded by quotations (some song names have multiple artists or unexpectedly long names).
