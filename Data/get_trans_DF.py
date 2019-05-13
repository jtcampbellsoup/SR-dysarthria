# This file reads in the raw transcript data, organizes it into a pandas DF, then saves
# it as a CSV

import numpy as np
import pandas as pd
import os

rootdir = os.getcwd() + '/RawTranscripts'
trans_DF = pd.DataFrame()
for filename in os.listdir(rootdir):
    f = open(rootdir + '/' + filename)
    text = f.read().split()
    text[:] = [i for i in text if i != '.']
    text.pop(0)
    trans_dict = {}
    for i in range(int(len(text)/2)):
        label = text[i*2][text[i*2].find('/') + 1: text[i*2].find('.lab')]
        trans = text[i*2+1].lower()
        trans_dict[label] = trans
    trans_DF_temp = pd.DataFrame(trans_dict.items(), columns = ['label', 'word'])
    splits = trans_DF_temp.label.str.split('_', expand = True)
    trans_DF_temp = trans_DF_temp.assign(P1 = splits[0], P2 = splits[1], P3 = splits[2], P4 = splits[3],
                          control = np.where(trans_DF_temp.label.str[0] == 'C', 1, 0))
    trans_DF_temp = trans_DF_temp.assign(gender = np.where((trans_DF_temp.P1.str[0] == 'M') | (trans_DF_temp.P1.str[1] == 'M'), 'M', 'F'))
    trans_DF = trans_DF.append(trans_DF_temp)
trans_DF = trans_DF.sort_values(['P1','P2','P3','P4']).reset_index(drop = True)
cols = list(trans_DF)
cols.append(cols.pop(cols.index('word')))
trans_DF = trans_DF[cols]

# split into train/dev/test
np.random.seed(100)
trans_DF = trans_DF.assign(train = np.where((trans_DF.P1 == 'F04') | (trans_DF.P1 ==
                            'M14') | (trans_DF.P1 == 'M16') | (trans_DF.P1 == 'CM13'), 0,
                            1))
devind = np.random.rand(trans_DF.shape[0])
trans_DF = trans_DF.assign(dev = np.where((devind <= 0.6) & (trans_DF.train == 0) & (
    trans_DF.P1 != 'CM13'), 1, 0))
trans_DF = trans_DF.assign(test = np.where((trans_DF.train == 0) & (trans_DF.dev == 0), 1,
                                           0))
trans_DF.to_csv(os.getcwd() + '/trans_DF.csv')