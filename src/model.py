from pymongo import MongoClient
import pymongo

from config.Config import Config as config
from db import DB
import facebook

class Model:
    def __init__(self):
        self._con = config()
        self._db = DB()

    def getFacebookUserInfo(self, access_token):
        graph = facebook.GraphAPI(access_token=access_token, version="3.1")
        user = None
        try : 
            user = graph.get_object('me')
        except :
            pass
        print(user)
        return user

    def