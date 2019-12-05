from peewee import *
from for_vk.entity.SettingDataBase import dbhandle

class Wall(Model):
    domain = CharField(null=False)
    id = IntegerField(null=False)
    type = CharField(null=False)
    error = IntegerField(null=False)




    class Meta:
        database = dbhandle


# def __init__(self,domain,id,type,error=0):
    #     self.link=domain
    #     self.id=id
    #     self.type=type
    #     self.error=error