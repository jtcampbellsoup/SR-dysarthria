# this file formats the scp and txt files that are pointed to in the config files that
# we use for data processing

import os
import pandas as pd

# get transcriptDF
trans_DF = pd.read_csv(os.getcwd() + '/Data/trans_DF.csv')

trans_DF_train = trans_DF[trans_DF.train == 1]
trans_DF_dev = trans_DF[trans_DF.dev == 1]
trans_DF_test = trans_DF[trans_DF.test == 1]

f = open('Data/audio/train.scp', 'w')
for index, row in trans_DF_train.iterrows():
    f.write(row['label'] + ' ' + 'Data/audio/train/' + row['fileloc'] + '\n')
f = open('Data/audio/dev.scp', 'w')
for index, row in trans_DF_dev.iterrows():
    f.write(row['label'] + ' ' + 'Data/audio/dev/' + row['fileloc'] + '\n')
f = open('Data/audio/test.scp', 'w')
for index, row in trans_DF_test.iterrows():
    f.write(row['label'] + ' ' + 'Data/audio/test/' + row['fileloc'] + '\n')
f = open('Data/audio/train.txt', 'w')
for index, row in trans_DF_train.iterrows():
    f.write(row['label'] + ' ' + row['phonemes'] + '\n')
f = open('Data/audio/dev.txt', 'w')
for index, row in trans_DF_dev.iterrows():
    f.write(row['label'] + ' ' + row['phonemes'] + '\n')
f = open('Data/audio/test.txt', 'w')
for index, row in trans_DF_test.iterrows():
    f.write(row['label'] + ' ' + row['phonemes'] + '\n')
