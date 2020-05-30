from pymongo import MongoClient


class Connection:
    @staticmethod
    def connect(collection_name: str):
        #my_connection = MongoClient(host="localhost", port=27017, username="YOUR_USERNAME", password="YOUR_PASSWORD")
        my_connection = MongoClient(host="localhost", port=27017)
        return my_connection["movies"][collection_name]
