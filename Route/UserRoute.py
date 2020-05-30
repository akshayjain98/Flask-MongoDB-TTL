from __main__ import app
from flask import jsonify, request
from Model.UserModel import UserModel

user = UserModel()


@app.route("/registration", methods=["POST"])
def registration():
    user_detail = request.get_json()
    return user.user_registration(user_detail)


@app.route("/login", methods=["POST"])
def login():
    user_detail = request.get_json()
    return user.user_login(user_detail["email"], user_detail["password"])
