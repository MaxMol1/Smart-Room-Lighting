from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string

class SentimentModel:
    # Returns sentiment of song lyrics - Positive, Neutral, or Negative
    def getSongSentiment(self, lyrics):
        sid = SentimentIntensityAnalyzer()
        tokenizer = RegexpTokenizer(r'\w+')
        # TODO: consider stopword removal
        stop_words = stopwords.words('english') + list(string.punctuation) + ["ve", "nt", "s", "d", "ll", "re", "m", "verse", "chorus", "outro"]

        positive = 0
        negative = 0
        neutral = 0

        # split node app output into a list
        lyrics = lyrics.split('\n')[1:-1]
        lyrics_tokenized = []
        
        # tokenize and remove stopwords
        for line in lyrics:
            parsed_line = tokenizer.tokenize(line.lower())
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

        # if song has very little lyrics
        if not negative + positive + neutral:
            return 'Neutral'

        percent_positive = (positive/float(negative + positive + neutral))*100
        percent_negative = (negative/float(negative + positive + neutral))*100

        if abs(percent_positive - percent_negative) < 2:
            # neutral
            return 'Neutral'
        elif percent_positive > percent_negative:
            # positive songs
            return 'Positive'
        else:
            # negative songs
            return 'Negative'
