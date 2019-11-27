from peewee import *
from entity.SettingDataBase import dbhandle

class Photo(Model):
    id = IntegerField(null=False)
    idpost = IntegerField(null=False)
    idwall = IntegerField(null=False)
    # где находится - в посте или комментариях
    where = CharField(null=False)
    # бинарник фото
    photobytes = BigBitField(null=False)
    # photobytes = CharField(null=False)
    # ссылка по которой скачивали фото
    url = CharField(max_length=1000,null=False)
    # если она находится в комментариях
    idcomment = IntegerField(null=False)
    class Meta:
        database = dbhandle









    # def __init__(self,id,idpost,idwall,where,photobytes,url,idcomment=False):
    #     self.id=id
    #     self.idpost=idpost
    #     self.idwall = idwall
    #     # где находится - в посте или комментариях
    #     self.where=where
    #     # бинарник фото
    #     self.photobytes=photobytes
    #     # ссылка по которой скачивали фото
    #     self.url=url
    #     # если она находится в комментариях
    #     self.idcomment=idcomment