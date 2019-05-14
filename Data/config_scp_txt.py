import os
import pandas as pd

# get transcriptDF
trans_DF = pd.read_csv(os.getcwd() + '/trans_DF.csv')

trans_DF_train = trans_DF[trans_DF.train == 1]
trans_DF_dev = trans_DF[trans_DF.dev == 1]
trans_DF_test = trans_DF[trans_DF.test == 1]

f = open('audio/train.scp', 'w')
for index, row in trans_DF_train.iterrows():
    f.write(row['label'] + ' ' + row['fileloc'] + '\n')
f = open('audio/dev.scp', 'w')
for index, row in trans_DF_dev.iterrows():
    f.write(row['label'] + ' ' + row['fileloc'] + '\n')
f = open('audio/test.scp', 'w')
for index, row in trans_DF_test.iterrows():
    f.write(row['label'] + ' ' + row['fileloc'] + '\n')
f = open('audio/train.txt', 'w')
for index, row in trans_DF_train.iterrows():
    f.write(row['label'] + ' ' + row['word'] + '\n')
f = open('audio/dev.txt', 'w')
for index, row in trans_DF_dev.iterrows():
    f.write(row['label'] + ' ' + row['word'] + '\n')
f = open('audio/test.txt', 'w')
for index, row in trans_DF_test.iterrows():
    f.write(row['label'] + ' ' + row['word'] + '\n')