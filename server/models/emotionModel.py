import text2emotion as te
import re

def getSongEmotion(lyrics):
    if lyrics == '':
        raise Exception('FAILED to receive lyrics')

    # process lyrics
    parsedLyrics = re.sub("[\(\[].*?[\)\]]", "", lyrics)
    
    # call function
    emotionScore = te.get_emotion(parsedLyrics.lower())

    # return highest emotion
    return (max(emotionScore, key = emotionScore.get))

def getSongColor(emotion):
    options = {
        'Happy': {'r': 255, 'g': 255, 'b': 128},
        'Angry': {'r': 255, 'g': 102, 'b': 102},
        'Surprise': {'r': 153, 'g': 255, 'b': 170},
        'Sad': {'r': 128, 'g': 212, 'b': 255},
        'Fear': {'r': 204, 'g': 102, 'b': 255}
    }
    
    return options[emotion]
