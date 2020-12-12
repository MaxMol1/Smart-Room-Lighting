# Sound-Reactive-LED

### Fetching Lyrics
Navigate to the lyrics directory and run ./wrapper_fetch_lyrics.sh with the arguments for song name and artist to fetch lyrics off Genius.

```./wrapper_fetch_lyrics.sh "Bohemian Rhapsody" "Queen"```

### Classifying Song
Navigate to the models directory and run python3 model.py with the same arguments as described above to classify a song as **positive**, **negative**, or **mellow**.

**Note:** Make sure to enter the song name and artist exactly (some song names have multiple artists or unexpectedly long names).
