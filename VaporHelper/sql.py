import os
import sys

from peewee import Model, PostgresqlDatabase, Proxy
from playhouse.db_url import connect
from VaporHelper import ENV

import psycogreen.gevent; psycogreen.gevent.patch_psycopg() # pylint: disable=E0601


REGISTERED_MODELS = []

database = Proxy()

class BaseModel(Model):
    class Meta:
        database = database
    
    @staticmethod
    def register(cls):
        REGISTERED_MODELS.append(cls)
        return cls

def init_db():
    if ENV == 'local':
        database.initialize(PostgresqlDatabase(
            'vaporbot',
            user='MBJ'
        ))
    elif ENV == 'docker':
        database.initialize(connect(os.environ.get('DB_POSTGRESQL') or 'sqlite:///default.db'))
    else:
        sys.exit(1337)
    for model in REGISTERED_MODELS:
        model.create_table(True)
