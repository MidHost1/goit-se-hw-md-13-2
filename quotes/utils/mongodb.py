from mongoengine import connect
import configparser
import os


def get_mongodb_connection():
    uri = os.getenv('MONGO_URI') 
    connect(host=uri, alias='default')