import bson
from pymongo import MongoClient
from uuid import UUID
from app.owner import Owner
from os import environ as env
from bson.binary import Binary


class OwnerFinder:
    def __init__(self, params):
        self.__mongo_host = params['mongo_host']
        self.__mongo_port = params['mongo_port']
        self.__mongo_db = params['mongo_db']

        self.__mongo_client = MongoClient(self.__mongo_host, self.__mongo_port)
        db = self.__mongo_client[self.__mongo_db]
        self.__collection = db['owners']

    @staticmethod
    def find(owner_id: UUID) -> Owner:
        mongo_host = env.get('MONGO_HOST', 'localhost')
        mongo_port = int(env.get('MONGO_PORT', 27017))
        mongo_db = env.get('MONGO_DB', 'mayaprotect')

        mongo_client = MongoClient(mongo_host, mongo_port)
        db = mongo_client[mongo_db]
        collection = db['owners']
        req = {'uuid': Binary.from_uuid(owner_id)}
        owner_data = collection.find_one(req)
        return Owner(owner_data)
