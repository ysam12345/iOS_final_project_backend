from pymongo import MongoClient
import pymongo
import json

from config.Config import Config as config
from db import DB
import facebook
import time
from apns import APNs, Frame, Payload

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

    def addAccount(self, access_token, device_token):
        user = None
        result = None
        try :
            user = self.getFacebookUserInfo(access_token)
        except :
            pass
        # if access token is valid
        if user!=None :
            # connect db
            client = self._db.connect()
            iOS_final_project_db = client["iOS_final_project"]
            accountDoc = {"facebook_id" : user["id"] , "name" : user["name"], "access_token" : access_token, "device_token" : device_token}
            # upsert : insert if not exist / update if exist
            result = iOS_final_project_db["account"].update_one({'facebook_id':user["id"]}, {"$set": accountDoc}, upsert=True)
        return result 

    def getUserByToken(self, access_token):
        user = None
        result = None
        try :
            user = self.getFacebookUserInfo(access_token)
        except :
            pass
        # if access token is valid
        if user!=None :
            # connect db
            client = self._db.connect()
            iOS_final_project_db = client["iOS_final_project"]
            result = iOS_final_project_db["account"].find_one({'facebook_id':user["id"]})
        return result 



    def getUserNotificationList(self, access_token):
        user = None
        result = None
        try :
            user = self.getUserByToken(access_token)
        except :
            pass
        # if access is exist in db
        if user!=None :
            print(user["facebook_id"])

            # connect db
            client = self._db.connect()
            iOS_final_project_db = client["iOS_final_project"]
            result = list(iOS_final_project_db["notification_list"].find({'facebook_id':user["facebook_id"]}, {'_id': False}))

            print(result)
        return result

    def addNotification(self, access_token, notification_data):
        user = None
        result = None
        try :
            user = self.getUserByToken(access_token)
        except :
            pass
        # if access is exist in db
        if user!=None and notification_data!=None :
            print(user["facebook_id"])
            notification_data = json.loads(notification_data)
            # connect db
            client = self._db.connect()
            iOS_final_project_db = client["iOS_final_project"]
            result = iOS_final_project_db["notification_list"].insert({'facebook_id': user["facebook_id"],'data': notification_data}, {'_id': False})

            print(result)
        return result 

    def removeNotification(self, access_token, notification_data):
        user = None
        result = None
        try :
            user = self.getUserByToken(access_token)
        except :
            pass
        # if access is exist in db
        if user!=None and notification_data!=None :
            print(user["facebook_id"])
            notification_data = json.loads(notification_data)
            # connect db
            client = self._db.connect()
            iOS_final_project_db = client["iOS_final_project"]
            result = iOS_final_project_db["notification_list"].delete_one({'facebook_id': user["facebook_id"],'data': notification_data})

            print(result)
        return result 

    def sendRemoteNotification(self, device_token, content):
        apns = APNs(use_sandbox=True, cert_file='./config/dev-cert.pem', key_file='./config/dev-key-noec.pem')

        # Send an iOS 10 compatible notification
        token_hex = device_token
        payload = Payload(alert=content, sound="default", badge=1, mutable_content=True)
        apns.gateway_server.send_notification(token_hex, payload)

    def sendRemoteNotificationToAllAccount(self, access_token, content):
        user = None
        result = None
        try :
            user = self.getUserByToken(access_token)
        except :
            pass
        # if access is exist in db
        if user!=None and content!=None :
            print(user["facebook_id"])
            # connect db
            client = self._db.connect()
            iOS_final_project_db = client["iOS_final_project"]
            result = list(iOS_final_project_db["account"].find({}, {'_id': False}))
            for i in result:
                self.sendRemoteNotification(result[i].device_token, content)
            print(result)
        return result 