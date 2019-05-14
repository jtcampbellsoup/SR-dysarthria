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
for wavefile in trainwavefiles:
    match = trans_DF.loc[trans_DF.label == wavefile[0:-4]]
    if match.shape[0] == 1:
        count += 1
for wavefile in devwavefiles:
    match = trans_DF.loc[trans_DF.label == wavefile[0:-4]]
    if match.shape[0] == 1:
        count += 1
for wavefile in testwavefiles:
    match = trans_DF.loc[trans_DF.label == wavefile[0:-4]]
    if match.shape[0] == 1:
        count += 1
print(count)