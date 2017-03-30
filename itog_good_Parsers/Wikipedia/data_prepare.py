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

def UCIdict(dictionary):
    dc = ['сраныйвыбросблин']
    for i in range(1,len(dictionary)):
        dc.append(dictionary[i])
    return(dc)

def UCItor(corpus):
    allw = 0
    for item in corpus:
        allw += len(item)
    doc = [len(corpus),len(dictionary)-1,allw]
    for i in range(len(corpus)):
        for item in corpus[i]:
            m = i + 1
            s = str(m) +' '+ str(item[0]+1) +' '+ str(item[1]) 
            doc.append(s)
    return(doc)


start_time = time.time()  # Включаем замеритель времени! 

print 'Подгружаю данные после стеминга:'
dict = corpora.Dictionary()
dictionary = dict.load('data_stem/dictionary_stem.dict')
corpus = corpora.MmCorpus('data_stem/corpus_stem.mm')

print 'Делаю словарь совместным с ARTM'
dct = UCIdict(dictionary)
file_obj = open("ARTM/vocab.wikistem.txt", "w")
file_obj.writelines(digit + '\n' for digit in map(str, dct))
file_obj.close()

print 'Делаю корпус совместным с ARTM'
txt = UCItor(corpus)
file_obj = open("ARTM/docword.wikistem.txt", "w")
file_obj.writelines(digit + '\n' for digit in map(str, txt))
file_obj.close()

print "--- %s seconds ---" % (time.time() - start_time)  #выводим время работы кода
print 'Усё'



start_time = time.time()  # Включаем замеритель времени! 
print 'Подгружаю данные после лемматизации:'
dict = corpora.Dictionary()
dictionary = dict.load('data_lemm/dictionary_lemm.dict')
corpus = corpora.MmCorpus('data_lemm/corpus_lemm.mm')


print 'Делаю словарь совместным с ARTM'
dct1 = UCIdict(dictionary)
file_obj = open("ARTM/vocab.wikilemm.txt", "w")
file_obj.writelines(digit + '\n' for digit in map(str, dct1))
file_obj.close()

print 'Делаю корпус совместным с ARTM'
txt1 = UCItor(corpus)
file_obj = open("ARTM/docword.wikilemm.txt", "w")
file_obj.writelines(digit + '\n' for digit in map(str, txt1))
file_obj.close()

print "--- %s seconds ---" % (time.time() - start_time)  #выводим время работы кода






# print 'Подгружаю словари'
# dict = corpora.Dictionary()
# dictionary = dict.load('dicts/wikidict.dict')
# corpus = corpora.MmCorpus('dicts/wikicorpus.mm')



