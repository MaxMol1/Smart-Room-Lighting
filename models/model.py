import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('vader_lexicon')
import string

import os
import subprocess

from termcolor import colored

def process_artists(artists):
    sid = SentimentIntensityAnalyzer()
    tokenizer = RegexpTokenizer(r'\w+')
    # TODO: consider stopword removal
    # stop_words = stopwocrds.words('english') + list(string.punctuation) + ["ve", "nt", "s", "d", "ll", "re", "m", "verse", "chorus", "outro"]

    for song,artist in artists.items():
        positive = 0
        negative = 0
        neutral = 0

        # get lyrics for a song from an artist
        os.chdir('../lyrics')
        output = subprocess.check_output(["node", "genius.js", song, artist])
        os.chdir('../models')

        # TODO: no output - stop loop

        # split node app output into a list
        lyrics = output.split(b'\n')[1:-1]
        lyrics_tokenized = []
        
        # tokenize and remove stopwords
        for line in lyrics:
            parsed_line = line.decode('utf-8')
            parsed_line = tokenizer.tokenize(parsed_line.lower())
            # parsed_line = [w for w in parsed_line if not w in stop_words and not w.isnumeric()]
            parsed_line = " ".join(parsed_line)
            lyrics_tokenized.append(parsed_line)

        # iterate through each line in lyrics
        for line in lyrics_tokenized:
            comp = sid.polarity_scores(line)
            comp = comp['compound']
            if comp >= 0.5:
                positive += 1
            elif comp > -0.5 and comp < 0.5:
                neutral += 1
            else:
                negative += 1

        percent_positive = (positive/float(negative + positive + neutral))*100
        percent_negative = (negative/float(negative + positive + neutral))*100

        red = "\033[31m"
        green = "\033[32m"
        blue = "\033[34m"
        if percent_positive > percent_negative:
            print(colored(song, 'blue'), 'by', colored(artist, 'blue'), 'is a ', colored('positive', 'green'), 'song')
            print(percent_positive, 'vs', percent_negative)
        else:
            print(colored(song, 'blue'), 'by', colored(artist, 'blue'), 'is a ', colored('negative', 'red'), 'song')
            print(percent_negative, 'vs', percent_positive)

def main():
    artists = {
        'happy' : 'pharrellwilliams',
        'scartissue' : 'Red Hot Chili Peppers',
        'blu' : 'Jon Bellion',
        'loveride' : 'christianfrench',
        'revenge' : 'xxxtentacion',
        'fromtime' : 'drake',
        'aintnobodylovesmebetter' : 'felixjaehn',
        'lovelies' : 'khalidnormani',
        'psycho' : 'postmalone',
        'allgirlsarethesame' : 'juicewrld',
        'jealous' : 'giannikyle',
        'yellow' : 'coldplay',
        'come & go' : 'juice wrld',
    }

    process_artists(artists=artists)
    
if __name__ == "__main__":
    main()
