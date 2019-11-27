import vk_api
import sys
from entity.Wall import Wall
from entity.photo import Photo
from entity.Comment import Comment
from entity.Post import Post
import requests
import datetime


# login, password = sys.argv[1], sys.argv[2]
login, password = '79169686822', 'bios88005553535bios'
vk_session = vk_api.VkApi(login, password)

try:
    vk_session.auth(token_only=True)
except:
    print(vk_api.AuthError)


vk = vk_session.get_api()



#  получение одной записи
def onepost(post,idwall=False,type=False):

    somepost = Post.create(id=post['id'],
                     subsidiarypost=idwall,
                    idwall=post['owner_id'],
                    iduser=post['from_id'],
                    text=post['text'],
                    date=datetime.datetime.fromtimestamp(post['date']),
                    likes=post['likes']['count'],
                    reposts=post['reposts']['count'],
                    foto=0)

    # somepost.save()

    # если в записи есть фотки
    if 'attachments' in post:
        for i in post['attachments']:
            if i['type']=='photo':
                somepost.foto+=1
                somephoto=Photo.create(id=i['photo']['id'],
                                idcomment=0,
                                idpost=post['id'],
                                idwall=post['owner_id'],
                                where='post',
                                photobytes=requests.get(i['photo']['sizes'][0]['url']).content,
                                url=i['photo']['sizes'][0]['url'])
                # somephoto.save()
                print(somephoto)
    print(somepost)
    # если в записи есть комменты
    # доступно только для нерепостнутых записей
    # будем собирать только первые комменты без комментов комментов
    if type:
        if type=='user':
        # если это группа
            allcomments=vk.wall.getComments(owner_id=idwall,post_id=somepost.id)
        elif type=='group':
        # если это профиль
            allcomments=vk.wall.getComments(owner_id=-idwall,post_id=somepost.id)
        for i in allcomments['items']:
            somecomment=Comment.create(id=i['id'],
                                idwall=idwall,
                                text=i['text'],
                                idpost=somepost.id)
            # somecomment.save()
            print(somecomment)
            # смотрим нааличие там фото
            if 'attachments' in i:
                for j in i['attachments']:
                    if j['type'] == 'photo':
                        somephoto = Photo.create(id=j['photo']['id'],
                                          idpost=post['id'],
                                          idwall=post['owner_id'],
                                          where='comment',
                                          photobytes=requests.get(i['photo']['sizes'][0]['url']).content,
                                          url=i['photo']['sizes'][0]['url'],
                                          idcomment=i['id'])
                        # somephoto.save()
                        print(somephoto)









    # если это репост
    if 'copy_history' in post:
        onepost(post['copy_history'],post['id'])
        somepost.subsidiarypost=post['copy_history']['id']
    return somepost







#функция получения  всех записей стены по ссылке
def readfromwall(link):


    # процесс получения id - делаем это потому что в случае ошибки на нас не вернутся айдишник
    domain = link.split('/')[-1]
    a=vk.utils.resolveScreenName(screen_name=domain)
    id=a['object_id']
    typeobjct=a['type']



    response = vk.wall.get(domain=domain,count=10000)  # Используем метод wall.get

    # проверим есть ли ошибка - если есть то запишем но уже не сохраняя посты
    if 'error_code' in response:
        somawall = Wall.create(domain=domain,id= id,type= typeobjct,error=response['error_code'])
        # somawall.save()
    else:
        somawall = Wall.create(domain=domain,id= id,type= typeobjct,error=0)
        # somawall.save()




    print(somawall)




    if somawall.error==0:
#если ошибки при получении стены не было то идем дальше и смотрим что на стене
        for post in response['items']:
            print('-----------------------------------------------------------------------------------------------------------')
            somepost=onepost(post,somawall.id,somawall.type)







if __name__=="__main__":
    Comment.create_table()
    Photo.create_table()
    Post.create_table()
    Wall.create_table()
    readfromwall('https://vk.com/id13757332')

