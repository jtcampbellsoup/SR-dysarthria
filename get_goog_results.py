import os
import speech_recognition as sr
import pandas as pd

dirname = os.getcwd() + '/Data/audio'
folders = [folder for folder in os.listdir(dirname)]

goog_results = pd.DataFrame(columns=['label', 'transcript'])

r = sr.Recognizer()

for folder in folders:
    wavefiles = [f for f in os.listdir(dirname + '/' + folder) if f[-4:] == '.wav']
    labels = []
    transcripts = []

    for wavefile in wavefiles:
        with sr.AudioFile(dirname + '/' + folder + '/' + wavefile) as source:
            audio = r.record(source)
        try:
            word = r.recognize_google(audio)
            print(wavefile[0:-4] + ': ' + word)
            transcripts.append(word)
            labels.append(wavefile[0:-4])
        except sr.UnknownValueError:
            print(wavefile[0:-4] + ': 0')
            transcripts.append('0')
            labels.append(wavefile[0:-4])
    results = pd.DataFrame(data={'label': labels, 'transcript': transcripts})
    goog_results = goog_results.append(results)

goog_results.to_csv(os.getcwd() + '/Results/goog_results.csv')