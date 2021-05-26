from pymongo import MongoClient
from pprint import pprint
import config

client = MongoClient(config.MONGODB_URL_ROUTER)
db = client.test


def connect():
    try:
        db.command("serverStatus")
    except Exception as e:
        print(e)
    else:
        print("You are connected!")
