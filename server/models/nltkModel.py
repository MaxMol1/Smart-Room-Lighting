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

from termcolor import colored

import os
import subprocess
import sys

def process_artists(song, artist):
    sid = SentimentIntensityAnalyzer()
    tokenizer = RegexpTokenizer(r'\w+')
    # TODO: consider stopword removal
    stop_words = stopwords.words('english') + list(string.punctuation) + ["ve", "nt", "s", "d", "ll", "re", "m", "verse", "chorus", "outro"]

    positive = 0
    negative = 0
    neutral = 0

    # get lyrics for a song from an artist
    os.chdir('../server')
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
        parsed_line = [w for w in parsed_line if not w in stop_words and not w.isnumeric()]
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

    if percent_positive == 0.0 and percent_negative == 0.0:
        # accounts for most EDM
        print(colored(song, 'blue'), 'by', colored(artist, 'blue'), 'is a ', colored('positive', 'green'), 'song')
        print(percent_positive, 'vs', percent_negative)
    elif abs(percent_positive - percent_negative) < 2:
        # songs between positive/negative
        print(colored(song, 'blue'), 'by', colored(artist, 'blue'), 'is a ', colored('mellow', 'cyan'), 'song')
        print(percent_positive, 'vs', percent_negative)
    elif percent_positive > percent_negative:
        # positive songs
        print(colored(song, 'blue'), 'by', colored(artist, 'blue'), 'is a ', colored('positive', 'green'), 'song')
        print(percent_positive, 'vs', percent_negative)
    else:
        # negative songs
        print(colored(song, 'blue'), 'by', colored(artist, 'blue'), 'is a ', colored('negative', 'red'), 'song')
        print(percent_negative, 'vs', percent_positive)

def main():
    process_artists(song=sys.argv[1], artist=sys.argv[2])
    
if __name__ == "__main__":
    main()
