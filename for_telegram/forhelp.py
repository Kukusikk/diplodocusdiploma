from telethon import TelegramClient, connection
import socks
import asyncio
from telethon import functions

api_id = 977079                  # API ID (получается при регистрации приложения на my.telegram.org)
api_hash = "ee798991396203bd491eef71a3ba96bc"              # API Hash (оттуда же)



# Необходимо предварительно авторизоваться, чтобы был создан файл second_account,
# содержащий данные об аутентификации клиента.
proxy_ip="192.169.202.106"
port=42319

client = TelegramClient('session23', api_id, api_hash, proxy=(socks.SOCKS5, str(proxy_ip), port))
client.start()





def readfromkanal():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(client(functions.contacts.SearchRequest(q='diplomdiplodog', limit=100)))
    result = result.chats[0]
    posts = loop.run_until_complete(client.get_messages(result,limit=1000))
    loop.close()

    for post in posts:
        print(post.message)





if __name__=="__main__":
    readfromkanal()