import vk_api
from for_vk.entity.Wall import Wall
from for_vk.entity.photo import Photo
from for_vk.entity.Comment import Comment
from for_vk.entity.Post import Post
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
def onepost(post,repost,idwall=False,type=False):

    if repost:
        somepost = Post.create(id=post['id'],
                             subsidiarypost=idwall,
                            idwall=post['owner_id'],
                            iduser=post['from_id'],
                            text=post['text'],
                            date=datetime.datetime.fromtimestamp(post['date']),
                            likes=0,
                            reposts=0,
                            foto=0,
                            subsidiaryowner_id=0,
                            classification=0,testingclassification=0)
    else:
        somepost = Post.create(id=post['id'],
                               subsidiarypost=idwall,
                               idwall=post['owner_id'],
                               iduser=post['from_id'],
                               text=post['text'],
                               date=datetime.datetime.fromtimestamp(post['date']),
                               likes=post['likes']['count'],
                               reposts=post['reposts']['count'],
                               subsidiaryowner_id=0,
                               foto=0, classification=0,testingclassification=0)
    # except:
    #     print(9)
    # если id стены и автора поста не совпадают то кидаем его в очередь на парсинг
    if post['owner_id']!=post['from_id']:
        queuewall.append(post['from_id'])

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
        try:
            if type=='user':
            # если это группа

                allcomments=vk.wall.getComments(owner_id=idwall,post_id=somepost.id)
            elif type=='group':
            # если это профиль
                allcomments=vk.wall.getComments(owner_id=-idwall,post_id=somepost.id)

            for i in allcomments['items']:
                if 'text' in i:
                    somecomment=Comment.create(id=i['id'],
                                        idwall=idwall,
                                        text=i['text'],
                                        idpost=somepost.id)

                # somecomment.save()
                # print(somecomment)
                # смотрим нааличие там фото
                if 'attachments' in i:
                    for j in i['attachments']:
                        if j['type'] == 'photo':
                            somephoto = Photo.create(id=j['photo']['id'],
                                              idpost=post['id'],
                                              idwall=post['owner_id'],
                                              where='comment',
                                              photobytes=requests.get(j['photo']['sizes'][0]['url']).content,
                                              url=j['photo']['sizes'][0]['url'],
                                              idcomment=i['id'])
                            # somephoto.save()
                            print(somephoto)
        except:
            pass









    # если это репост
    if 'copy_history' in post:
        onepost(post['copy_history'][0],True,post['copy_history'][0]['owner_id'])
        somepost.subsidiarypost=post['copy_history'][0]['id']
        somepost.subsidiaryowner_id=post['copy_history'][0]['owner_id']
        queuewall.append(post['copy_history'][0]['from_id'])
    return somepost






queuewall=[]
#функция получения  всех записей стены по домену страницы
#id,  type, domain
def readfromwall(helpdict):



    # процесс получения id - делаем это потому что в случае ошибки на нас не вернутся айдишник
    # domain = link.split('/')[-1]
    if helpdict['domain']:
        domain=helpdict['domain']
        a=vk.utils.resolveScreenName(screen_name=helpdict['domain'])
        id=a['object_id']
        typeobjct = a['type']
    else:
        id = helpdict['id']
        if id>0:
            typeobjct = 'user'
            domain=vk.user.users.get(user_ids=-id, fields='screen_name')['response'][0]['screen_name']
        else:
            typeobjct = 'group'
            domain=vk.groups.getById(group_id=id, fields='screen_name')['response'][0]['screen_name']


    # если с этой стены мы еще не читали то читаем
    if newwallaboutdomain(id):
        return






    try:
        response = vk.wall.get(domain=helpdict['domain'],count=10000)  # Используем метод wall.get

        # проверим есть ли ошибка - если есть то запишем но уже не сохраняя посты
        if 'error_code' in response:
            somawall = Wall.create(domain=helpdict['domain'],id= id,type= typeobjct,error=response['error_code'])

        else:
            somawall = Wall.create(domain=helpdict['domain'],id= id,type= typeobjct,error=0)
        print(somawall)
    except:
        somawall = Wall.create(domain=helpdict['domain'], id=id, type=typeobjct, error=1)




    if somawall.error==0:
#если ошибки при получении стены не было то идем дальше и смотрим что на стене
        for post in response['items']:
            print('-----------------------------------------------------------------------------------------------------------')
            somepost=onepost(post,False,somawall.id,somawall.type)


def takelistdomain(file):
    listdomain=[]
# читаем из файла каждую строку - это наш запрос к поиску групп
    with open(file, 'r') as f:
        for line in f:
            a=vk.groups.search(q=line)
    # идем по этому списку и делаем запросы с желанием получить эти группы
            for onegroup in vk.groups.search(q=line)['items']:
                listdomain.append(onegroup['screen_name'])
    return listdomain

# ????????????????????????????????????????????????
#функция проверки наличия у нас еще памяти
def limitramm():
    import psycopg2
    conn = psycopg2.connect(dbname='diplodog', user='test_user',
                            password='qwerty', host='localhost', port=5434)
    cursor = conn.cursor()
    cursor.execute('SELECT pg_size_pretty( pg_database_size( diplodog ) )')
    records = cursor.fetchall()
    cursor.close()
    conn.close()
# функция проверки есть у нас эта стена уже в базе или еще нет
# обезопасет нас от бесконечной рекурсии
# вернуть true если с таким именем стена в базе уже есть
def newwallaboutdomain(domain):
    if len(Wall.select().where(Wall.domain == domain)):
        return True
    return False
def newwallaboutid(id):
    if len(Wall.select().where(Wall.id == id)):
        return True
    return False




if __name__=="__main__":
    #имя файла для ключевых слов, изначально для которых ищем группы
    keywoldsfile='beginlist'
    Comment.create_table()
    Photo.create_table()
    Post.create_table()
    Wall.create_table()
    # limitramm()
    list_of_seach=takelistdomain(keywoldsfile)

    # по ключевым словам получаем список доменов, по которым ведется дальнейший парсинг
    for i1 in list_of_seach:
        readfromwall({'domain':i1,'type':False})
    while len(queuewall):
        for j1 in queuewall:
            queuewall.remove(j1)
            readfromwall({'id':j1,'domain':False})

