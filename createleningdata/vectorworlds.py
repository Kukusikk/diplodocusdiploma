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
from gensim.models.word2vec import Word2Vec
# данный скрипт будет  создаваться для создания тестовой выбоки с загрузкой уже существующей модели векторов
# Поле с признаком:
# текст поста, в случае если он репостнут то берем текст еще и из начального поста
# Дата поста
# домен стены
# количество лайков в случае если он репостнут то суммируем их
# количество репостов в случае если он репостнут то суммируем их
# количество фото в случае если он репостнут то суммируем их



#Сначала считаем все тексты и создадим обучающу выборку. Где объектом станут упорядоченные
# слова из тескта, а label-ом класс, к которому относится текст.


# в качестве параметра получаем количество постов, которые нужно отдать

def createleningdata():
#подключаемсяк бд
    x,y=[],[]
    # идем по таблице со всеми постами


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
            domenwall=''
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
        x.append([correcttext(text),correctdate(date),correcttext(domenwall), likes,reposts, foto ])
        y.append(classification)

    cursor.close()
    conn.close()
    return x,y


# корректируем текст сообщения - удаляем абзацы, разбиваем на слова, удаляем знаки припенания и приводим все к нижнему регистру
def correcttext(text):
    listtext=[]
    # удаляем все абзацы из сообщения
    # удаляем . , ! ? ( ) ; :
    text=re.sub(r"[\n,\.,;:!\?-]", "", text)
    return re.findall(r'\w+',text.lower())


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
#функция создания итоговой обучающей выборки
def creatingleningvector():
    X,Y=createleningdata()
    # загрузим модель которая у нас уже была сделана при создании обучающей выборки
    model = Word2Vec.load("/home/fuckinggirl/PycharmProjects/untitled5/createleningdata/word2vec.model")
# Для каждого слова из теста мы имеем соответсвующий ему вектор
# Для решения задачи
# классификации каждый текст преобразуем к среднему по векторам, соответсвующим словам из
# словаря, которые есть в данном тексте (если слова нет в тексте, то берем нулевой вектор). Это
# преобразование реализуется методом transform класса mean vectorizer
    result = []
    z=7
    for i in X:
        if z:
            z-=1
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
            try:
                i[2]=np.mean(model[i[2][0]],axis=0)
            except:
                i[2]=np.mean([np.zeros(100)],axis=0)
            result.append(i[0].tolist()+[i[1]]+i[2].tolist()+[i[3],i[4],i[5]])
    return result, Y


