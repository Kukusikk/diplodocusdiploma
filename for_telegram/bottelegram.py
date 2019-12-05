# from telethon import TelegramClient, connection
from io import BytesIO

import requests
import socks
import asyncio
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.types import PeerChannel

from for_telegram.entity.kanal import kanal
from for_telegram.entity.message import message
from for_telegram.entity.photo import photo

api_id = 977079                  # API ID (получается при регистрации приложения на my.telegram.org)
api_hash = "ee798991396203bd491eef71a3ba96bc"              # API Hash (оттуда же)



# Необходимо предварительно авторизоваться, чтобы был создан файл second_account,
# содержащий данные об аутентификации клиента.
proxy_ip="192.169.202.106"
port=42319

client = TelegramClient('session4', api_id, api_hash, proxy=(socks.SOCKS5, str(proxy_ip), port),timeout=66)
client.start()




# очередь из каналов которые надо просмотреть
queuekanal=[]
# функция исследование одного канала и запоминание его и его сообщений в бд
def seachinonekanal(kanal_):
    # запоминаем в бд инфу о канале


    somakanal = kanal.create(domain=kanal_.title, id=kanal_.id)
    # получение всех постов с канала
    posts = client.get_messages(kanal_, limit=1000)
    for post in posts:
        # смотрим есть ли в посте фото
        # запоминаем фото
        # пишем их количество
        photoid=0
        if post.media:
            photoid = 1
            image_buf = BytesIO()
            post.download_media(image_buf )
            image = image_buf.getvalue()

            # photo.create(id=post.media.photo.id,idmassage=post.id, idkanal=kanal_.id,photobytes=image )
            id9=post.media.photo.id
            photo.create(id=id9 ,idmassage=post.id, idkanal=kanal_.id, photobytes=image)





        # если эта запись  репостнута то заносим в список обхода канал с которого репостили
        if post.forward:
            message.create(id_kanal=kanal_.id, id=post.id, text=post.message,subsidiarymassage=post.forward.channel_post, subsidiaryidkanal=post.forward.channel_id, fotoid=photoid)
            queuekanal.append(post.forward.chat)
        else:
            message.create(id_kanal=kanal_.id, id=post.id, text=post.message, subsidiarymassage=0,
                           subsidiaryidkanal=0, fotoid=photoid)







def takelistdomain(file):
# читаем из файла каждую строку - это наш запрос к поиску групп
    with open(file, 'r') as f:
        for line in f:
            result = client(functions.contacts.SearchRequest(q=line,limit=100))
            result = result.chats
    # вернем список каналов для их обхода
    return result

# проверка проходили лы мы этот канал уже или еще нет
def newkanalaboutid(id):
    if len(kanal.select().where(kanal.id == id)):
        return True
    return False

if __name__=="__main__":
    # создадим таблицы в бд
    photo.create_table()
    message.create_table()
    kanal.create_table()
    # имя файла для ключевых слов, изначально для которых ищем группы
    keywoldsfile = 'beginlisttelegram'
    queuekanal=takelistdomain(keywoldsfile)
    while len(queuekanal):
        # пока есть какие каналы обходить - обходим их
        for i in queuekanal:
            if not newkanalaboutid(i.id):
                # если этот канал мы еще не обходили
                # то идем и парсим его
                seachinonekanal(i)
            queuekanal.remove(i)

















