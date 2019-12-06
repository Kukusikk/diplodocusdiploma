
from peewee import *
from for_vk.entity.SettingDataBase import dbhandle

class Post(Model):
    id = IntegerField(null=False)
    # на чьей стене
    idwall = IntegerField(null=False)
    # кто написал
    iduser = IntegerField(null=False)
    text = TextField(null=False)
    date = DateField(null=False)
    likes = IntegerField(null=False)
    reposts = IntegerField()
    # в случае если запись репосттнута то тут тоже пост от репоста
    subsidiarypost = IntegerField(null=False)
    # здесь пишем количесво фото к посту
    foto = IntegerField(null=False)
    #классификация поста
    classification=IntegerField(null=False)







    # def __init__(self,id,idwall,iduser,text,date,likes,reposts,subsidiarypost=False,foto=0 ):
    #     self.id=id
    #     # на чьей стене
    #     self.idwall = idwall
    #     # кто написал
    #     self.iduser=iduser
    #     self.text=text
    #     self.date=date
    #     self.likes=likes
    #     self.reposts=reposts
    #     #в случае если запись репосттнута то тут тоже пост от репоста
    #     self.subsidiarypost=subsidiarypost
    #     # здесь пишем количесво фото к посту
    #     self.foto=foto
    class Meta:
        database = dbhandle

