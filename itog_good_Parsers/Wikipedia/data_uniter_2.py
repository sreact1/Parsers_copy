# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 

import sys  
reload(sys) 
sys.setdefaultencoding('utf8')

import numpy as np
from gensim import corpora,models
import itertools
import gensim
import time

names = ['_error.npy','_titles.npy','_words.npy']

# делай раз - стеминг!

print('Создаю единый вектор из статей')
def un(words,i):
    a = np.load('data_stem/'+str(i)+names[2])
    a = list(a)
    words.extend(a)
    return(words)

words1 = []
words1 = un(words1,0)
words1 = un(words1,1)
print len(words1)

print 'Делаю первый словарь и корпус'
dictionary1 = corpora.Dictionary(words1)
print dictionary1 
corpus1 = [dictionary1.doc2bow(text) for text in words1]
words1 = []

words2 = []
words2 = un(words2,2)
words2 = un(words2,3)
print len(words2)

print 'Делаю второй словарь и корпус'
dictionary2 = corpora.Dictionary(words2)
print dictionary2
corpus2 = [dictionary2.doc2bow(text) for text in words2]
words2 = []

print 'Добавляю первый словарь к нулевому'
dt01 = dictionary1.merge_with(dictionary2)
print dictionary1

print 'Сливаю соответствующие им корпуса'
merged_corpus = itertools.chain(corpus1, dt01[corpus2])
cp01 = [item for item in merged_corpus]

dictionary1.save('data_stem/dictionary_stem.dict')
corpora.MmCorpus.serialize('data_stem/corpus_stem.mm', cp01)


# То же самое с лемматизацией!

def un(words,i):
    a = np.load('data_lemm/'+str(i)+names[2])
    a = list(a)
    words.extend(a)
    return(words)

words1 = []
words1 = un(words1,0)
words1 = un(words1,1)
print len(words1)

print 'Делаю первый словарь и корпус'
dictionary1 = corpora.Dictionary(words1)
print dictionary1 
corpus1 = [dictionary1.doc2bow(text) for text in words1]
words1 = []

words2 = []
words2 = un(words2,2)
words2 = un(words2,3)
print len(words2)

print 'Делаю второй словарь и корпус'
dictionary2 = corpora.Dictionary(words2)
print dictionary2
corpus2 = [dictionary2.doc2bow(text) for text in words2]
words2 = []

print 'Добавляю первый словарь к нулевому'
dt01 = dictionary1.merge_with(dictionary2)
print dictionary1

print 'Сливаю соответствующие им корпуса'
merged_corpus = itertools.chain(corpus1, dt01[corpus2])
cp01 = [item for item in merged_corpus]

dt01.save('data_lemm/dictionary_lemm.dict')
corpora.MmCorpus.serialize('data_lemm/corpus_lemm.mm', cp01)



