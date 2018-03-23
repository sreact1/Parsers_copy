import requests
from bs4 import BeautifulSoup
import re
import time
import pickle
import numpy as np
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from multiprocessing import Pool
import nltk
from nltk.corpus import stopwords
import pymorphy2
import wikipedia
wikipedia.set_lang("ru")


start_time = time.time() # время работы кода 

print("Начинаю работу")

# открываем файл с названиями
with open('data_raw/wiki_names.pickle', 'rb') as handle:
    collection = pickle.load(handle)

print(len(collection['Заглавия']))  # ого как их много! =) 

# Эта функция токенезирует безошибочную статью и выдаёт список составляющих её слов
def Ttknzer(name):
    text = wikipedia.page(name)
    text = text.content
    raw = text.lower()
    visible_raw = re.sub(u"[^а-я., ]", "", raw) # очистка от хлама
    tokens = tokenizer.tokenize(visible_raw)
    return(tokens)

# Эта функция удаляет из токенизированной статьи все стоп-слова. Остальные слова они с помощью лемматизации приводит к хорошему виду. 
stop = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()

def Stop_Lemma(vect):
    out1 = [item for item in vect if not item in stop]
    out2 = [morph.parse(item)[0].normal_form for item in out1]
    return(out2)

# Эта функция объединяет два предыдущих шага. Так будет проще засунуть её в Map. 

def Big_Function(name):
    x1 = Ttknzer(name)
    x2 = Stop_Lemma(x1)
    return(x2)

# Эта функция берёт на вход коллекцию и выдаёт список ошибок и список из нумпаевских списков составляющих, а также список заголовков. 

def Map(zagol):
    words = [ ]
    titles = [ ]
    errors = [ ] 
    for i in range(len(zagol)):
        try:
            newtxt = Big_Function(zagol[i])
            titles.append(zagol[i])
            words.append(newtxt)
        except Exception:
            errors.append(zagol[i])
    itog = [errors,titles,words]
    return(itog)

# Соединение данных воедино
def Reduce(l):
    words1 = [ ]
    titles1 = [ ]
    errors1 = [ ]
    for i in range(len(l)):
        errors1.extend(l[i][0])
        titles1.extend(l[i][1])
        words1.extend(l[i][2])
    itog = [errors1,titles1,words1]
    return(itog)



# Делим весь список из имён на 4 части
parts = [round(len(collection['Заглавия'])/4)*i for i in range(4)]
parts.append(len(collection['Заглавия']))
wikinames = [collection['Заглавия'][parts[i]:parts[i+1]] for i in range(4)]

for j in range(4):
    current = wikinames[j]
    len(current)
    # Делим весь наш список на входные потоки по сколько-то тысяч статей
    def Part(shift1,shift2):
        now = current[shift1:shift2]
        return(now)
    
    a = [int(item) for item in np.linspace(0,len(current)-(len(current))/110, num=110)]
    a.append(len(current))
    curlist = [Part(a[i],a[i+1]) for i in range(len(a)-1)]
    print(len(curlist))
    print(sum([len(curlist[i]) for i in range(110)]))
    print("Начинаю map-шаг")
    
    if __name__ == '__main__':
    	with Pool(110) as p:
        	l = p.map(Map, curlist)
          
    print("Начинаю reduce-шаг")  
    itog = Reduce(l)   # Соединяем всё это дело воедино!
    l =0               # Наверное так будет полегче компухтеру
    # Парочка сток для душевного спокойствия
    print(len(itog))
    print(len(itog[0]))
    print(len(itog[1]))
    print(len(itog[2]))
        
    # Сохраняем!
    print("Сохраняю данные") 
    np.save('data_lemm/'+str(j)+'_error.npy',np.array(itog[0]))
    np.save('data_lemm/'+str(j)+'_titles.npy',np.array(itog[1]))
    np.save('data_lemm/'+str(j)+'_words.npy',np.array(itog[2]))
    itog = 0           # Зануляем на всякий случай! 
    print("Всё сделал, перехожу ко второй итерации!") 

print("--- %s seconds ---" % (time.time() - start_time))  #время работы кода

