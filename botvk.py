import vk_api
import sys

""" Пример получения последнего сообщения со стены """


login, password = sys.argv[1], sys.argv[2]
vk_session = vk_api.VkApi(login, password)

try:
    vk_session.auth(token_only=True)
except:
    print(vk_api.AuthError)


vk = vk_session.get_api()


""" VkApi.method позволяет выполнять запросы к API. В этом примере
    используется метод wall.get (https://vk.com/dev/wall.get) с параметром
    count = 1, т.е. мы получаем один последний пост со стены текущего
    пользователя.
"""

def readfromwall():
    print("input link : ")
    link=input()
    # print(link)


    # link='https://vk.com/art.jpgg'
    # процесс получения id
    id = link.split('/')[-1]
    if not id.replace('id', '').isdigit():
        id=vk.utils.resolveScreenName(screen_name=id)['object_id']
    else:
        id=id[2:]


    response = vk.wall.get(owner_id=id,count=10000)  # Используем метод wall.get

    for post in response['items']:
        print(post['text'])
        if 'copy_history' in post:
            print(post['copy_history'][0]['text'])






if __name__=="__main__":
    readfromwall()