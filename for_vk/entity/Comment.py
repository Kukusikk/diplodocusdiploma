from peewee import *
from for_vk.entity.SettingDataBase import dbhandle


class Comment(Model):
    id = IntegerField(null=False)
    idwall = IntegerField(null=False)
    text = TextField(null=False)
    # id поста
    idpost = IntegerField(null=False)

    # def __init__(self, id, idwall, text, idpost):
    #     self.id=id
    #     self.idwall=idwall
    #     self.text=text
    #     # id поста
    #     self.idpost=idpost

    class Meta:
        database = dbhandle
