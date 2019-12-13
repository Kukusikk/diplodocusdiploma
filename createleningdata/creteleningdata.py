# тут будет происходить разметка уже имеющихся данных, которые лежат в базе данных с помощью алгоритмов word2vec
# идея состоит в том, чтобы по созданной уже модели world2vec создать для имеющихся у нас постов классификацию на основе
# значения уже имеющегося вектора

import re
from collections import defaultdict
import psycopg2
from gensim.models import word2vec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
from sklearn.feature_extraction.text import TfidfVectorizer



def createleningdata():
#подключаемсяк бд
    x=[]
    # идем по таблице со всеми постами


    conn = psycopg2.connect(dbname='diplodog', user='test_user',
                            password='qwerty', host='localhost', port=5434)
    cursor = conn.cursor()
    cursor.execute('SELECT id, text, idwall, subsidiarypost,subsidiaryowner_id,idwall from post')
    records = cursor.fetchall()
    # идем по каждому посту
    for onepost in records:
        id=onepost[0]
        idwall=onepost[2]
        text=onepost[1]
        subsidiarypost=onepost[3]
        subsidiaryowner_id=onepost[4]
        idwall = onepost[5]
        if idwall < 0:
            idwall = -idwall
        # берем домен стены
        cursor.execute('SELECT domain from Wall where id={} '.format(idwall))
        try:
            domenwall = cursor.fetchall()[0][0]
        except:
            # если эта группа еще не была обойдена
            domenwall = ''
        if subsidiarypost:
# если запись репостнута то идем и берем текст из репоста и количество фоток тоже
            cursor.execute('SELECT  text  from post where id={} and idwall={}'.format(subsidiarypost,subsidiaryowner_id))
            primarysource=cursor.fetchall()
            if len(primarysource):
            #     мы могли не обойти эту группу, чтобы не вылететь делаем проверку
                text +=' '+ primarysource[0][0]
        #формируем итоговую выборку текстов
        x.append([correcttext(text),id,idwall, domenwall] )


    cursor.close()
    conn.close()
    return x


# корректируем текст сообщения - удаляем абзацы, разбиваем на слова, удаляем знаки припенания и приводим все к нижнему регистру
def correcttext(text):
    listtext=[]
    # удаляем все абзацы из сообщения
    # удаляем . , ! ? ( ) ; :
    text=re.sub(r"[\n,\.,;:!\?-]", "", text)
    return re.findall(r'\w+',text.lower())



def fit(listworld):

    tfidf=TfidfVectorizer(analyzer=lambda listworld:listworld)
    try:
        tfidf.fit(listworld)
        max_idf=max(tfidf.idf_)
        word2weight=defaultdict(
            lambda :max_idf,
            [(w ,tfidf.idf_[i]) for w,i in tfidf.vocabulary_.items()]
        )
        return word2weight
    except:
        return [0 for i in range(len(listworld))]

def keywords():
    listkeywords=[]
    filename='keywords'
    with open(filename, 'r') as f:
        for line in f:
            listkeywords.append(re.sub(r"\n", "", line))
    return listkeywords

# проверяем схож ли данный вектор на вектора с нашей любимой суецидальной тематикой
def whatkategory(a):
    j=max(list(a))
    if j:
       n=model.most_similar(positive=[a], topn=10)
       listsravnen=keywords()
       for i in n:
           if i[0] in listsravnen:
               return 1
    return 0




X=createleningdata()

# Для того чтобы обучить классификатор каждый объект должен быть задан вектором числовых признаков. Именно для решения этой проблемы очень
# удобно применить Word2Vec и перевести слова в числовые вектора
# туда должны закинуть все предложения и имена доменов как предложения
dataforvectoring=[]
for i in X:
    dataforvectoring.append(i[0])
    dataforvectoring.append(i[3])

model=word2vec.Word2Vec(dataforvectoring,sg=1, size=100, window=3,  workers=4)

# Теперь для каждого слова из теста мы имеем соответсвующий ему вектор
# Для решения задачи
# классификации каждый текст преобразуем к среднему по векторам, соответсвующим словам из
# словаря, которые есть в данном тексте (если слова нет в тексте, то берем нулевой вектор). Это
# преобразование реализуется методом transform класса mean vectorizer.
# print(model['MUSIC'])


# получим список слов по которым нам нужно

for i in X:
    listvector = []

    for world in i[0]:
        if world in model:
            # идем по каждому слову
            # и добавляем его вектор в массив
            try:
                listvector.append(model[world]*fit(i[0])[world])
            except:
                listvector.append(fit(i[0]))

    a=np.mean(listvector  or [np.zeros(100)],axis=0)
    i[0]=a


    conn2 = psycopg2.connect(dbname='diplodog', user='test_user',
                            password='qwerty', host='localhost', port=5434)
    cursor2 = conn2.cursor()
    if whatkategory(a):
        # если категория текста не нулевая
        cursor2.execute('UPDATE post SET classification=1 WHERE ID={} and idwall={}'.format(i[1],i[2]))
    else:
        cursor2.execute('UPDATE post SET classification=0 WHERE ID={} and idwall={}'.format(i[1], i[2]))
    conn2.commit()
    cursor2.close()
    conn2.close()


# сохраним полученную модель
model.save("word2vec.model")







