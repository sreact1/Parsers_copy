import requests
from bs4 import BeautifulSoup
import re
import time
import pickle
import numpy as np


start_time = time.time() #время работы кода 

# Парсер имён статей
def Titles_Founder(soup):
    dd = soup.findAll("ul",{"class":"mw-allpages-chunk"})
    new_dd = dd[0].findAll("li")
    
    href = [item.a["href"] for item in new_dd]
    n1 = len(href)-1
    href = href[:n1]
    
    titles = [item.a["title"] for item in new_dd]
    n2 = len(titles)-1
    tit = titles[n2] # Следующее имя для парсера
    titles = titles[:n2]
    
    dictionary = {'Заглавия':titles,'Ссылки':href,'Контрольные цифры':[len(new_dd),n1+1,n2+1],'Следующее имя':[tit]} 
    return(dictionary)


# Итоговый код, который будет выдёргивать столько статей из списка сколько нам будет нужно!

collection = {'Заглавия':[],'Ссылки':[],'Контрольные цифры':[],'Следующее имя':[]}
# Эта строка нужна для того, чтобы начался цикл while. Как только в списке останется только одно имя
# для дозаписи, это будет означать что рубрикация иссякла и цикл прервётся. 
names = {'Заглавия':[1],'Ссылки':[],'Контрольные цифры':[],'Следующее имя':[]}
main = "https://ru.wikipedia.org/w/index.php?title=Служебная:Все_страницы&from="
page = main + "!" + "&hideredirects=1"     #Тэг для стартовой страницы

k = 1 #Счётчик для количества отработанных страниц
while len(names['Заглавия'])!= 0:
# for i in range(3):                    # строка нужна была для тестов кода
    response = requests.get(page)       # выгружает данные по ссылке
    html = response.content             # переводит их в читаемый формат, который можно вывести на экран
    soup = BeautifulSoup(html,"lxml")   # отсекает кучу всяких ненужных вещей и запускает поиск по тегам в html 
    names = Titles_Founder(soup)        # вытаскиваем из html всё, что нас интересует! 
    # Расширяем нашу коллекцию! 
    collection['Заглавия'].extend(names['Заглавия'])
    collection['Ссылки'].extend(names['Ссылки'])
    collection['Контрольные цифры'].extend(names['Контрольные цифры'])
    collection['Следующее имя'].extend(names['Следующее имя'])
    # Перепрыгиваем на следующую страничку!
    page = main + names["Следующее имя"][0] + "&hideredirects=1"
    if k % 10 == 0:  #Код будет выводить каждые 200 итераций число
        print(k)      #И текущее следующее имя, чтобы не запутаться
        print(names['Следующее имя'][0])
    k += 1

with open('wiki_names.pickle', 'wb') as handle:
    pickle.dump(collection, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('wiki_names.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)

print(collection == unserialized_data)    


print("--- %s seconds ---" % (time.time() - start_time))  #время работы кода






