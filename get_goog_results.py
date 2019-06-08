# File finds uses the Google CLoud speech recognition toolkit to get word translations of the audio files in our test set

import os
import speech_recognition as sr
import pandas as pd

folder = os.getcwd() + 'nabu/Data/audio/test'

r = sr.Recognizer()

wavefiles = [f for f in os.listdir(folder) if f[-4:] == '.wav']
labels = []
transcripts = []

for wavefile in wavefiles:
    try:
        with sr.AudioFile(folder + '/' + wavefile) as source:
            audio = r.record(source)
        try:
            word = r.recognize_google(audio).lower()
            print(wavefile[0:-4] + ': ' + word)
            transcripts.append(word)
            labels.append(wavefile[0:-4])
        except sr.UnknownValueError:
            print(wavefile[0:-4] + ': NA')
            transcripts.append('NA')
            labels.append(wavefile[0:-4])
    except:
        print('audio file corrupt')
        os.remove(folder + '/' + wavefile)

goog_results = pd.DataFrame(data={'label': labels, 'transcript': transcripts})

goog_results.to_csv(os.getcwd() + 'nabu/Results/goog_results.csv')
