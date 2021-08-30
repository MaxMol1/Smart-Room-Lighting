import text2emotion as te
import re

class EmotionModel:
    # Returns top two emotions from song lyrics
    def getSongEmotion(self, lyrics):
        if lyrics == '' or lyrics == 'This is an instrumental!':
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
