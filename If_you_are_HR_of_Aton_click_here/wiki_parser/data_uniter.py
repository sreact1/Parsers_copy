import numpy as np

names = ['_error.npy','_titles.npy','_words.npy']

print('Создаю единый вектор из ошибок')
error = []
for i in range(4):
    a = np.load('data_lemm/'+str(i)+names[0])
    a = list(a)
    error.extend(a)

print('Количество ошибок:')
print(len(error))
np.save('data_lemm/lem_errors',np.array(error))


print('Создаю единый вектор из заголовков')
titles = []
for i in range(4):
    a = np.load('data_lemm/'+str(i)+names[1])
    a = list(a)
    titles.extend(a)

print('Количество заголовков:')
print(len(titles))
np.save('data_lemm/lem_titles',np.array(titles))

print('Частота ошибок:')
print(len(error)/(len(titles)+len(errors)))


# Немного самоиронии: эх! Сейчас бы несколько раз скопировать один и тот же код...


print('Создаю единый вектор из ошибок')
error = []
for i in range(4):
    a = np.load('data_stem/'+str(i)+names[0])
    a = list(a)
    error.extend(a)

print('Количество ошибок:')
print(len(error))
np.save('data_stem/stem_errors',np.array(error))


print('Создаю единый вектор из заголовков')
titles = []
for i in range(4):
    a = np.load('data_stem/'+str(i)+names[1])
    a = list(a)
    titles.extend(a)

print('Количество заголовков:')
print(len(titles))
np.save('data_stem/stem_titles',np.array(titles))

print('Частота ошибок:')
print(len(error)/(len(titles)+len(error)))



























