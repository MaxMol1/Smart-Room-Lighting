# Sound-Reactive-LED

### Introduction

This is a project aiming to map songs to colors based on the sentiment of the lyrics. These colors are then displayed on an LED strip via communication over wifi with an ESP8266 microcontroller in a sound-reactive manner.

### Fetching Lyrics
Navigate to the lyrics directory and run ./wrapper_fetch_lyrics.sh with the arguments for song name and artist to fetch lyrics using the Genius API.

```./wrapper_fetch_lyrics.sh "Bohemian Rhapsody" "Queen"```

### Classifying Song
Navigate to the models directory and run python3 model.py with the same arguments as described above to classify a song as **positive**, **negative**, or **mellow**.

**Note:** Make sure to enter the song name and artist exactly (some song names have multiple artists or unexpectedly long names).

### TODO
1. Authenticate with Spotify to fetch current playing song in real time
2. Pipe output into sentiment classifier and translate response to certain colors
3. Set up communication between ESP8266 and classifier
3. Create a sound reactive visualization using fourier transformations
