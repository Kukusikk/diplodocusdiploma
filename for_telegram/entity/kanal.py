from peewee import *
from for_vk.entity.SettingDataBase import dbhandle

class kanal(Model):
    domain = CharField(null=False)
    id = IntegerField(null=False)
    # type = CharField(null=False)
    # error = IntegerField(null=False)





    class Meta:
        database = dbhandle
