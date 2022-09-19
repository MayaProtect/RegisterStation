from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from app.station import Station
import json


class RegisterStation:
    def __init__(self, params):
        self.__mongo_host = params['mongo_host']
        self.__mongo_port = params['mongo_port']
        self.__mongo_db = params['mongo_db']

        self.__app = Flask(__name__)
        self.__app.route('/stations', methods=['POST'])(self.__register)
        CORS(self.__app)

        self.__mongo_client = MongoClient(self.__mongo_host, self.__mongo_port)
        db = self.__mongo_client[self.__mongo_db]
        self.__collection = db['stations']

    @cross_origin()
    def __register(self):
        data = request.get_json()
        station = Station(data)
        result = self.__collection.insert_one(station.to_dict())
        if result.inserted_id:
            response = {
                "message": "Station registered with uuid {}".format(station.id)
            }
            return Response(json.dumps(response), status=201)
        else:
            response = {
                "code": 500,
                "message": "Station not registered"
            }
            return Response(json.dumps(response), status=500)

    def run(self):
        self.__app.run(host='0.0.0.0', port=3000)
