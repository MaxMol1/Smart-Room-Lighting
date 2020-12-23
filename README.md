# Sound-Reactive-LED

### Introduction

This is a project that uses localhost to show information in real time about songs that a Spotify user plays including the lyrics, genres, release date, and mood. It also includes a sentiment analyzer that maps colors to a song based on the sentiment of its lyrics.

This project supports communication over WiFi with an ESP8266 microcontroller for the purpose of broadcasting the colors of the current song to lights and LED strips to match the mood.

### Starting the Server

Navigate to the lyrics directory and run ```node app.js```. This will start up a server on localhost:3000 where you can log in with your spotify account. After doing so, click the button **Start Tracking** to see live results of the current song that you have playing.

### Classifying Song

Navigate to the models directory and run python3 model.py with the arguments for song name and artist to classify a song as **positive**, **negative**, or **mellow**.

**Note:** Make sure to enter the song name and artist exactly and surrounded by quotations (some song names have multiple artists or unexpectedly long names).
