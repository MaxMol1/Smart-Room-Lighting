import text2emotion as te
import re

class EmotionModel:
    # Returns top two emotions from song lyrics
    def getSongEmotion(self, lyrics):
        if lyrics == '' or lyrics == 'this is an instrumental!':
            raise Exception('FAILED to receive lyrics')
        
        # invoke test2emotion function
        emotionScore = te.get_emotion(lyrics)

        return sorted(emotionScore.items(), key=lambda x: x[1], reverse=True)
