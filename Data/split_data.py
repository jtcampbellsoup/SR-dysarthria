import os
import pandas as pd

dirname = os.getcwd() + '/audio'
folders = [folder for folder in os.listdir(dirname)]
folders.remove('train')
folders.remove('dev')
folders.remove('test')

testfolders = ['CM13', 'F04', 'M14', 'M16']
trainfolders = [i for i in folders if i not in testfolders]

# get transcriptDF
trans_DF = pd.read_csv(os.getcwd() + '/trans_DF.csv')

for folder in trainfolders:

    wavefiles = [f for f in os.listdir(dirname + '/' + folder) if f[-4:] == '.wav']

    for wavefile in wavefiles:
        os.rename(dirname + '/' + folder + '/' + wavefile, dirname + '/train/' + wavefile)

for folder in testfolders:
    wavefiles = [f for f in os.listdir(dirname + '/' + folder) if f[-4:] == '.wav']

    for wavefile in wavefiles:
        if trans_DF.loc[trans_DF.label == wavefile, 'test'] == 1:
            os.rename(dirname + '/' + folder + '/' + wavefile,
                      dirname + '/test/' + wavefile)
        else:
            os.rename(dirname + '/' + folder + '/' + wavefile,
                      dirname + '/dev/' + wavefile)