from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

class SentimentModel:
    # Returns sentiment of song lyrics - Positive, Negative, or Neutral
    def getSongSentiment(self, lyrics):
        sid = SentimentIntensityAnalyzer()

        # process lyrics
        lines = re.sub("[\(\[].*?[\)\]]", "", lyrics).lower().split('\n')
        lines = [line for line in lines if line]

        # keep track of positive, negative, or neutral sentences
        positive = 0
        negative = 0
        neutral = 0

        # iterate through each line in lyrics
        for line in lines:
            sentiment = sid.polarity_scores(line)
            if sentiment['compound'] >= 0.5:
                positive += 1
            elif sentiment['compound'] <= -0.5:
                negative += 1
            else:
                neutral += 1

        # if song has very little lyrics
        if not negative + positive + neutral:
            return 'Neutral'

        percent_positive = (positive/float(positive + negative + neutral))*100
        percent_negative = (negative/float(positive + negative + neutral))*100

        if abs(percent_positive - percent_negative) < 2:
            # neutral
            return 'Neutral'
        elif percent_positive > percent_negative:
            # positive songs
            return 'Positive'
        else:
            # negative songs
            return 'Negative'
