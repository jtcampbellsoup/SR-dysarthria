# removes invalid audio files
import os
import pandas as pd

trainfolder = os.getcwd() + '/audio/train'
devfolder = os.getcwd() + '/audio/dev'
testfolder = os.getcwd() + '/audio/test'

# get transcriptDF
trans_DF = pd.read_csv(os.getcwd() + '/trans_DF.csv')

trainwavefiles = [f for f in os.listdir(trainfolder) if f[-4:] == '.wav']
devwavefiles = [f for f in os.listdir(devfolder) if f[-4:] == '.wav']
testwavefiles = [f for f in os.listdir(testfolder) if f[-4:] == '.wav']

count = 0
labels = list(trans_DF.label)
for wavefile in trainwavefiles:
    if wavefile[0:-4] in labels:
        count += 1
        print(count)
    else:
        os.remove(os.getcwd()+'/audio/train/' + wavefile)
for wavefile in devwavefiles:
    if wavefile[0:-4] in labels:
        count += 1
        print(count)
    else:
        os.remove(os.getcwd()+'/audio/dev/' + wavefile)
for wavefile in testwavefiles:
    if wavefile[0:-4] in labels:
        count += 1
        print(count)
    else:
        os.remove(os.getcwd()+'/audio/test/' + wavefile)
print(count)
