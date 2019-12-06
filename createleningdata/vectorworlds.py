import re
from collections import defaultdict

from gensim.models import word2vec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta


# Поле с признаком:
# текст поста, в случае если он репостнут то берем текст еще и из начального поста
# Дата поста
# домен стены
# количество лайков в случае если он репостнут то суммируем их
# количество репостов в случае если он репостнут то суммируем их
# количество фото в случае если он репостнут то суммируем их



#Сначала считаем все тексты и создадим обучающу выборку. Где объектом станут упорядоченные
# слова из тескта, а label-ом класс, к которому относится текст.
from sklearn.feature_extraction.text import TfidfVectorizer

from createleningdata.createmeanvector import tfidf_vectorizes
from for_vk.entity.Post import Post


def createleningdata():
#подключаемсяк бд
    x,y=[],[]
    # идем по таблице со всеми постами
    import psycopg2

    conn = psycopg2.connect(dbname='diplodog', user='test_user',
                            password='qwerty', host='localhost', port=5434)
    cursor = conn.cursor()
    cursor.execute('SELECT idwall, text, date, likes, reposts, subsidiarypost, foto, classification from post')
    records = cursor.fetchall()
    # идем по каждому посту
    for onepost in records:
        idwall=onepost[0]
        if idwall<0:
            idwall=-idwall
    #берем домен стены
        cursor.execute('SELECT domain from Wall where id={}'.format(idwall))
        try:
            domenwall = cursor.fetchall()[0][0]
        except:
            # если эта группа еще не была обойдена
            continue
# если запись репостнута то идем и берем текст из репоста и количество фоток тоже
        text=onepost[1]
        date=onepost[2]
        likes=onepost[3]
        reposts=onepost[4]
        foto=onepost[6]
        classification=onepost[7]
        subsidiarypost=onepost[5]
        while subsidiarypost:
# если запись репостнута то идем и берем текст из репоста и количество фоток тоже
            cursor.execute('SELECT text, likes, reposts, subsidiarypost, foto from post where id={}'.format(onepost[5]))
            primarysource=cursor.fetchall()
            if len(primarysource):
            #     мы могли не обойти эту группу, чтобы не вылететь делаем проверку
                text += primarysource[0][0]
                likes += primarysource[0][1]
                reposts += primarysource[0][2]
                foto += primarysource[0][4]
                subsidiarypost=primarysource[0][3]
            else:
                subsidiarypost=0
        #формируем итоговую выборку
        x.append([correcttext(text),correctdate(date),[domenwall], likes,reposts, foto ])
        y.append(classification)

    cursor.close()
    conn.close()
    return x,np.array(y)


# корректируем текст сообщения - удаляем абзацы, разбиваем на слова
def correcttext(text):
    listtext=[]
    # удаляем все абзацы из сообщения
    text = re.sub(r"\n", "", text)
    return text.split(' ')


# корректируем дату в количество недель
def correctdate(date):
    return relativedelta(datetime.date.today(),date).weeks


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



X,Y=createleningdata()
print(6)
# Для того чтобы обучить классификатор каждый объект должен быть задан вектором числовых признаков. Именно для решения этой проблемы очень
# удобно применить Word2Vec и перевести слова в числовые вектора
# туда должны закинуть все предложения и имена доменов как предложения
dataforvectoring=[]
for i in X:
    dataforvectoring.append(i[0])
    dataforvectoring.append(i[2])
model=word2vec.Word2Vec(dataforvectoring)

# Теперь для каждого слова из теста мы имеем соответсвующий ему вектор
# Для решения задачи
# классификации каждый текст преобразуем к среднему по векторам, соответсвующим словам из
# словаря, которые есть в данном тексте (если слова нет в тексте, то берем нулевой вектор). Это
# преобразование реализуется методом transform класса mean vectorizer.
print(model['MUSIC'])
for i in X:
    # a=tfidf_vectorizes(np.array(i[0]))
# идем по каждому тексту
#     dim=len(next(iter(model.values())))
    listvector = []
    for world in i[0]:

        if world in model:
            # идем по каждому слову
            # и добавляем его вектор в массив
            try:
                listvector.append(model[world]*fit(i[0])[world])
            except:
                listvector.append(fit(i[0]))

    a=np.mean(listvector  or [np.zeros(len(i[0]))],axis=0)
    i[0]=a
    i[2]=model[i[2]]

# #########################################################################################################################################
# дальше идет посмтоение классификатора