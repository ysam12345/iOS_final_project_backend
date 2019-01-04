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
    user = model.getFacebookUserInfo(access_token)
    response = {"code":"200"}
    if user!=None :
        response["status"] = "ok"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
