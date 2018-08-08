from flask import Flask
from flask import jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask.json import JSONEncoder
from bson import json_util
from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet
from flask_cors import CORS

class MongoEngineJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
app.json_encoder = MongoEngineJSONEncoder
CORS(app)
# uncomment the following line if you are targeting a local installation of mongo db
# client = MongoClient("mongodb://127.0.0.1:27017")

#  comment out line 10 if you uncomment line 7
client = MongoClient("mongodb://db:27017")
db = client["sensorlogs"]

@app.route("/logs", methods=["POST"])
def create_log():
    try:
        req_payload = request.get_json()
        db.logs.insert_one(req_payload)

        return jsonify(req_payload)
    except Exception as e:
        msg = "failed saving log"
        return jsonify({
            "msg" : msg,
            "error": str(e)
        })


@app.route("/logs", methods=["GET"])
def list_logs():
    try:
        logs = db.logs.find()
        res_payload = [l for l in logs]

        return jsonify(res_payload)
    except Exception as e:
        msg = "failed fetching logs"
        return jsonify({
            "msg": msg,
            "error": str(e)
        })


def main():
    app.run(host="0.0.0.0", port=7000, debug=True)

if __name__ == '__main__':
    main()

