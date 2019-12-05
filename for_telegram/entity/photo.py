from peewee import *
from for_vk.entity.SettingDataBase import dbhandle

class photo(Model):
    id = BigIntegerField(null=False)
    idmassage = IntegerField(null=False)
    idkanal = IntegerField(null=False)
    # бинарник фото
    photobytes = BigBitField(null=False)


    class Meta:
        database = dbhandle
