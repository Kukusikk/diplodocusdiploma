user = 'test_user'
password = 'qwerty'
db_name = 'diplodog'
from peewee import *



dbhandle = PostgresqlDatabase(
    db_name, user=user,
    password=password,
    # host='localhost',
    host='diplodogdiplom',
    port=5432
)
dbhandle.connect()