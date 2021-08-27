import text2emotion as te
import re

# Returns top two emotions from song lyrics
def getSongEmotion(lyrics):
    if lyrics == '':
        raise Exception('FAILED to receive lyrics')

    # process lyrics
    parsedLyrics = re.sub("[\(\[].*?[\)\]]", "", lyrics)
    
    # invoke test2emotion function
    emotionScore = te.get_emotion(parsedLyrics.lower())

    # return two highest emotions
    firstEmotion = max(emotionScore, key = emotionScore.get)
    del emotionScore[firstEmotion]
    secondEmotion = max(emotionScore, key = emotionScore.get)

    return (firstEmotion, secondEmotion)
