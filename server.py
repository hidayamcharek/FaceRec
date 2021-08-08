from flask import Flask, json, request
from pymongo import MongoClient
from bson.json_util import dumps
import base64
import face_recognition
from flask_cors import CORS,cross_origin
import face_recognition 
from PIL import Image
import glob
from bson.objectid import ObjectId
from bson import json_util


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = MongoClient('mongodb+srv://klasi:klasiproject@cluster0.cs4qs.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.admin

mydb = client["myFirstDatabase"]
mycol = mydb["anteriorcurriculums"]
usersdb = mydb["users"]

api = Flask(__name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@api.route('/users', methods=['GET'])
@cross_origin()
def get_users():
    for i in mycol.find({"photo":{"$exists":True}}):
        print(i.get('photo'))
        g = open("out.jpg", "w")
        imgdata = base64.urlsafe_b64decode(i.get('photo')[22:len(i.get('photo'))+1])
        with open(str(i.get('user'))+'.jpg', 'wb') as f:
            f.write(imgdata)
    return "hello"

@api.route('/connect', methods=['GET','POST'])
@cross_origin()
def get_photo():
    
    print(request.get_json()['photo'])
    imgdata = base64.urlsafe_b64decode(request.get_json()['photo'][22:len(request.get_json()['photo'])+1])
    with open('aaaa.jpg', 'wb') as f:
        f.write(imgdata)
    image_list = []
    for filename in glob.glob(r'*.jpg'): #assuming gif
        im=Image.open(filename)
        image_list.append(im)
        print(filename)
        image_known = face_recognition.load_image_file(filename)
        known_face_encoding = face_recognition.face_encodings(image_known)[0]
        image_unknown = face_recognition.load_image_file('aaaa.jpg')
        unknown_face_encoding = face_recognition.face_encodings(image_unknown)[0]

        results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)

        if results[0]:
            return parse_json(usersdb.find_one({"_id":ObjectId(filename[0:len(filename)-4])}, {"role":0}))
        else:
            print('enta monhou')
            return json.dumps({"user":'no user'})
    return json.dumps({"yes":'yes'})

if __name__ == '__main__':
    api.run()