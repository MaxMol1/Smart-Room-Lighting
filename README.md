# Sound-Reactive-LED

### Introduction

This is a project that uses localhost to show information in real time about songs that a Spotify user plays including the lyrics, genres, release date, and mood. It also includes a sentiment analyzer that maps colors to a song based on the sentiment of its lyrics.

This project supports communication over WiFi with an ESP8266 microcontroller for the purpose of broadcasting the colors of the current song to lights and LED strips to match the mood.

### Setting Up

To begin, you need to create an API client using [Genius](https://genius.com/developers). Pick an app name and a website, and then generate an access token when you see your client id and client secret. Paste this in line 34 of ```./lyrics/public/js/genius.js```.

You also need to create a developer account with [Spotify](https://developer.spotify.com/dashboard/login). Create a new application and be sure to 1. Take your client id and paste that in line 8 of ```./lyrics/app.js``` and 2. set the redirect uri of the app to be localhost:3000/main/

Navigate to the lyrics directory and run ```npm install``` and once that finishes, launch localhost using: ```node app.js```. Navigate to localhost:3000 in your browser and log in with your Spotify account to use the application. Click the button **Start Tracking** to see live results of the current song that you have playing.

### Classifying Song

Navigate to the models directory and run python3 model.py with the arguments for song name and artist to classify a song as **positive**, **negative**, or **mellow**.

**Note:** Make sure to enter the song name and artist exactly and surrounded by quotations (some song names have multiple artists or unexpectedly long names).
