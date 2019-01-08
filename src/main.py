from flask import Flask, jsonify, request
from model import Model
import json

model = Model()


# init Flask 
app = Flask(__name__)

#Route
@app.route('/')
def index():
    return 'Hello World!'

@app.route('/getUserNotificationList', methods=['GET'])
def getUserNotificationList():
    access_token = request.args.get('facebook_token')
    userNotificationList = model.getUserNotificationList(access_token)
    response = {"code":"200"}
    if userNotificationList!=None :
        response["status"] = "ok"
        response["data"] = userNotificationList
        return json.dumps(response)
    else :
        response["code"] = "503"
        response["error"] = "invalid token"
        return json.dumps(response)
    
@app.route('/checkToken', methods=['GET'])
def checkToken():
    access_token = request.args.get('facebook_token')
    user = model.getFacebookUserInfo(access_token)
    response = {"code":"200"}
    if user!=None :
        response["status"] = "ok"
        return json.dumps(response)
    else :
        response["code"] = "503"
        response["error"] = "invalid token"
        return json.dumps(response)

@app.route('/addAccount', methods=['GET'])
def addAccount():
    access_token = request.args.get('facebook_token')
    device_token = request.args.get('device_token')
    result = model.addAccount(access_token, device_token)
    response = {"code":"200"}
    if result!=None :
        response["status"] = "ok"
        return json.dumps(response)
    else :
        response["code"] = "503"
        response["error"] = "invalid token"
        return json.dumps(response)

@app.route('/addNotification', methods=['GET'])
def addNotification():
    access_token = request.args.get('facebook_token')
    notification_data = request.args.get('notification_data')
    result = model.addNotification(access_token, notification_data)
    response = {"code":"200"}
    if result!=None :
        response["status"] = "ok"
        return json.dumps(response)
    else :
        response["code"] = "503"
        response["error"] = "invalid token"
        return json.dumps(response)

@app.route('/sendRemoteNotification', methods=['GET'])
def sendRemoteNotification():
    access_token = request.args.get('device_token')
    notification_data = request.args.get('content')
    result = model.sendRemoteNotification(access_token, notification_data)
    response = {"code":"200"}
    return "ok" 
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

