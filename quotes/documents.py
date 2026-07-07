from mongoengine import Document, StringField, ListField, ReferenceField, connect, disconnect
from django.conf import settings
import os


def init_db():
    try:
        disconnect()
        connect(host=os.getenv('MONGO_URI'))
    except Exception as e:
        print(f"Помилка підключення: {e}")

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    author = ReferenceField(Author)
    tags = ListField(StringField())
    quote = StringField(required=True)
    
    meta = {'collection': 'quote'}