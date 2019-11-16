from telethon import TelegramClient, connection
import socks
import asyncio


api_id = 977079                  # API ID (получается при регистрации приложения на my.telegram.org)
api_hash = "ee798991396203bd491eef71a3ba96bc"              # API Hash (оттуда же)



# Необходимо предварительно авторизоваться, чтобы был создан файл second_account,
# содержащий данные об аутентификации клиента.
proxy_ip="192.169.202.18"
port=2472

client = TelegramClient('session', api_id, api_hash, proxy=(socks.SOCKS5, str(proxy_ip), port))
client.start()





def readfromkanal():

    print("input link : ")
    kanal=input() # название канала для поиска там
    loop = asyncio.get_event_loop()
    dp = loop.run_until_complete(client.get_entity(kanal))
    posts = loop.run_until_complete(client.get_messages(dp,limit=1000))
    loop.close()

    for post in posts:
        print(post.message)





if __name__=="__main__":
    readfromkanal()






