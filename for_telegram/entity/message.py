from peewee import *
from for_vk.entity.SettingDataBase import dbhandle

class message(Model):
    text = CharField(null=False)
    id = IntegerField(null=False)
    id_kanal=IntegerField(null=False)
    # в случае если запись репосттнута то тут id этой записи
    subsidiarymassage = IntegerField(null=False)
    # в случае если запись репосттнута то тут id этого канала
    subsidiaryidkanal = IntegerField(null=False)
    # здесь пишем количесво фото к посту
    fotoid = IntegerField(null=False)





    class Meta:
        database = dbhandle
