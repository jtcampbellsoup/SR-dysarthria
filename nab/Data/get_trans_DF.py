# This file reads in the raw transcript data, organizes it into a pandas DF, then saves
# it as a CSV. Will also define and output the phonetic alphabet we will use.

import numpy as np
import pandas as pd
import os
import nltk

rootdir = os.getcwd() + '/Data/RawTranscripts'
trans_DF = pd.DataFrame()
for filename in os.listdir(rootdir):
    f = open(rootdir + '/' + filename)
    text = f.read().split()
    text[:] = [i for i in text if i != '.']
    text.pop(0)
    labels = []
    words = []
    for i in range(int(len(text)/2)):
        label = text[i*2][text[i*2].find('/') + 1: text[i*2].find('.lab')]
        word = text[i*2+1].lower()
        labels.append(label)
        words.append(word)
    trans_DF_temp = pd.DataFrame(data = {'label': labels, 'word': words})
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

# match data to associated file, add column for it
trainfiles = os.listdir(os.getcwd() + '/Data/audio/train')
devfiles = os.listdir(os.getcwd() + '/Data/audio/dev')
testfiles = os.listdir(os.getcwd() + '/Data/audio/test')

trans_DF = trans_DF.assign(fileloc = "NA")
print('size before: ', trans_DF.shape)
for i in range(trans_DF.shape[0]):
    if (trans_DF.loc[i, 'train'] == 1):
        if ((trans_DF.loc[i, 'label'] + '.wav') in trainfiles):
            trans_DF.loc[i, 'fileloc'] = trans_DF.loc[i, 'label'] + '.wav'
    if (trans_DF.loc[i, 'dev'] == 1):
        if ((trans_DF.loc[i, 'label'] + '.wav') in devfiles):
            trans_DF.loc[i, 'fileloc'] = trans_DF.loc[i, 'label'] + '.wav'
    if (trans_DF.loc[i, 'test'] == 1):
        if ((trans_DF.loc[i, 'label'] + '.wav') in testfiles):
            trans_DF.loc[i, 'fileloc'] = trans_DF.loc[i, 'label'] + '.wav'
trans_DF = trans_DF[trans_DF.fileloc != 'NA'].reset_index(drop = True)
print('size after: ', trans_DF.shape)

# find bad words (any word not in our corpus dictionary) remove files and the rows from
# the data frame
fulldict = nltk.corpus.cmudict.dict()
print(len(fulldict))
badwords = set()
allwords = fulldict.keys()
print(len(allwords))

count = 0
for word in trans_DF.word.unique():
    count += 1
    print(count)
    if word not in allwords:
        badwords.add(word)
print(badwords)

badrows = trans_DF[trans_DF.word.isin(badwords)].reset_index(drop = True)
trans_DF = trans_DF[~trans_DF.word.isin(badwords)].reset_index(drop = True)
print(badrows.shape)
print(trans_DF.shape)

for i in range(badrows.shape[0]):
    if badrows.loc[i,'train'] == 1:
        if os.path.isfile(os.getcwd()+'/Data/audio/train/'+ badrows.loc[i, 'fileloc']):
            os.remove(os.getcwd() + '/Data/audio/train/' + badrows.loc[i, 'fileloc'])
    if badrows.loc[i,'dev'] == 1:
        if os.path.isfile(os.getcwd()+'/Data/audio/dev/'+ badrows.loc[i, 'fileloc']):
            os.remove(os.getcwd() + '/Data/audio/dev/' + badrows.loc[i, 'fileloc'])
    if badrows.loc[i,'test'] == 1:
        if os.path.isfile(os.getcwd()+'/Data/audio/test/'+ badrows.loc[i, 'fileloc']):
            os.remove(os.getcwd() + '/Data/audio/test/' + badrows.loc[i, 'fileloc'])

phstringlist = []
mapdict = {}
for word in trans_DF.word.unique():
    phoneme = fulldict[word][0]
    phstring = " ".join(phoneme).lower()
    mapdict[word] = phstring
count = 0
for word in trans_DF.word:
    phstringlist.append(mapdict[word])
    count += 1
    print(count)
trans_DF['phonemes'] = phstringlist

trans_DF.to_csv(os.getcwd() + '/Data/trans_DF.csv')

alph = set()
for phon in trans_DF.phonemes:
    phonlist = phon.split()
    for phn in phonlist:
        alph.add(phn)

f = open(os.getcwd() + '/Data/alphabet.txt', 'w')
for a in alph:
    f.write(a + ' ')
f.close()

