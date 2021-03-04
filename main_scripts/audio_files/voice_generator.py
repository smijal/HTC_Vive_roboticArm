from playsound import playsound
from gtts import gTTS
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
#small script to generate various mp3 messages ( text to speech )
#save them at the same directory and use them later in the main script to output various audio messages
def say(text, name):
    tts = gTTS(text=text, lang="en")
    f_name = name+".mp3"
    filename = os.path.join(current_directory,f_name)
    tts.save(filename)
    #playsound(filename)

say("Moving... X,, axis", "x_axis")
