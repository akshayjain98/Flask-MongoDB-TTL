from Database.Connection import Connection
import jwt
from flask import jsonify


class UserModel:
    SECRET_KEY = "AKSHAYJAIN"

    def __init__(self):
        self.__user_collection = Connection.connect("user")

    def user_login(self, email, password):
        result = self.__user_collection.find_one(
            {"email": email, "password": password}, {"role": 1})
        if result:
            token = jwt.encode(
                {"user_id": str(result["_id"]), "role": result["role"]}, UserModel.SECRET_KEY)
            return jsonify({"token": str(token)}), 200
        else:
            return jsonify({"message": "Invalid Credential"}), 401

    def user_registration(self, user_detail):
        result = self.__user_collection.count_documents(
            {"email": user_detail["email"]})
        if result == 0:
            result = self.__user_collection.insert_one(user_detail)
            if result.inserted_id:
                return jsonify({"user_id": str(result.inserted_id)}), 200
            else:
                return jsonify({"error": "Registration Fail"}), 400
        else:
            return jsonify({"warning": "User Already exists"}), 400
