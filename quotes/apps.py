from django.apps import AppConfig
from mongoengine import connect, disconnect
import os

class QuotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quotes'

    def ready(self):
        db_uri = os.environ.get('MONGO_URI') 
        db_name = 'quotes_db_mongo' 

        disconnect(alias='default')
        connect(db=db_name, host=db_uri, alias='default')