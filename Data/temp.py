import os
import pandas as pd

folder = os.getcwd() + '/audio/dev'

# get transcriptDF
trans_DF = pd.read_csv(os.getcwd() + '/trans_DF.csv')

wavefiles = [f for f in os.listdir(folder) if f[-4:] == '.wav']

for wavefile in wavefiles:
    vals = trans_DF.loc[trans_DF.label == wavefile[0:-4], 'test'].values
    if vals.size != 0:
        if vals[0] == 1:
            os.rename(folder + '/' + wavefile,
                      os.getcwd() + '/audio/test/' + wavefile)