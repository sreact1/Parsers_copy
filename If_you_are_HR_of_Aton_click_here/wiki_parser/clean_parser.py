import requests
from bs4 import BeautifulSoup
import re
import time
import pickle
import numpy as np
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from multiprocessing import Pool
import wikipedia
wikipedia.set_lang("ru")


start_time = time.time() # время работы кода 

print("Начинаю работу")

# открываем файл с названиями
with open('wiki_names.pickle', 'rb') as handle:
    collection = pickle.load(handle)

print(len(collection['Заглавия']))  # ого как их много! =) 

# Эта функция токенезирует безошибочную статью и выдаёт список составляющих её слов
def Ttknzer(name):
    text = wikipedia.page(name)
    text = text.content
    raw = text.lower()
    tokens = tokenizer.tokenize(raw)
    return(tokens)

# Эта функция берёт на вход коллекцию и выдаёт список ошибок и составляющих
def Map(zagol):
    words = {}
    errornumbers = []
    for i in range(len(zagol)):
        try:
            words[zagol[i]]=Ttknzer(zagol[i])
        except Exception:
            errornumbers.append(zagol[i])
    itog = {'Тексты':words,'Ошибки':errornumbers}
    return(itog)

# Соединение данных воедино
def Reduce(l):
    txts = { }
    err = [ ]
    for i in range(len(l)):
        txts.update(list(l[i]['Тексты'].items()))
        err.extend(l[i]['Ошибки'])
    itog_dict = {'Тексты':txts,'Ошибки':err}
    return(itog_dict)


# Делим весь список из имён на 4 части
parts = [round(1362487/4)*i for i in range(4)]
parts.append(len(collection['Заглавия']))
wikinames = [collection['Заглавия'][parts[i]:parts[i+1]] for i in range(4)]

for j in range(4):
    curent = wikinames[j]
    len(curent)
    # Делим весь наш список на входные потоки по сколько-то тысяч статей
    def Part(shift1,shift2):
        now = curent[shift1:shift2]
        return(now)
    
    a = [int(item) for item in np.linspace(0,len(curent)-(len(curent))/70, num=70)]
    a.append(len(curent))
    curlist = [Part(a[i],a[i+1]) for i in range(len(a)-1)]
    print(len(curlist))
    print(sum([len(curlist[i]) for i in range(70)]))
    print("Начинаю map-шаг")
    
    if __name__ == '__main__':
    	with Pool(70) as p:
        	l = p.map(Map, curlist)
          
    print("Начинаю reduce-шаг")  
    itog = Reduce(l)   # Соединяем всё это дело воедино!
    l =0               # Наверное так будет полегче компухтеру
    # Парочка сток для душевного спокойствия
    print(len(itog))
        
    # Сохраняем!
    print("Сохраняю данные") 
    with open('data_raw/'+str(j)+'_part.pickle', 'wb') as handle:
        pickle.dump(itog, handle, protocol=pickle.HIGHEST_PROTOCOL) 
    itog = 0           # Зануляем на всякий случай!
    print("Всё сделал, перехожу ко второй итерации!") 

print("--- %s seconds ---" % (time.time() - start_time))  #время работы кода
















