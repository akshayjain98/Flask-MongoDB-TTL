from __main__ import app
from flask import jsonify, request
from Model.TheaterModel import TheaterModel

theater = TheaterModel()


@app.route("/addtheater", methods=["POST"])
def add_theater():
    theater_detail = request.get_json()
    return theater.add_theater(theater_detail["theater_name"], theater_detail["address"])


@app.route("/addmovie", methods=["POST"])
def add_movie():
    theater_detail = request.get_json()
    return theater.add_movie(theater_detail["theater_id"], theater_detail["movie_name"],
                             theater_detail["total_seat"], theater_detail["time_slot"])


@app.route("/seatavailability", methods=["GET"])
def check_seat_availability():
    theater_detail = request.get_json()
    return jsonify(theater.seat_availability(theater_detail["theater_id"], theater_detail["movie_id"],
                                             theater_detail["time_slot"]))


@app.route("/bookseats", methods=["POST"])
def book_seats():
    theater_detail = request.get_json()
    return theater.book_seat(theater_detail["theater_id"], theater_detail["movie_id"], theater_detail["user_id"],
                             theater_detail["seat_number"], theater_detail["time_slot"])


@app.route("/paymentprocess", methods=["POST"])
def payment_process():
    theater_detail = request.get_json()
    return theater.payment_process(theater_detail["theater_id"], theater_detail["movie_id"], theater_detail["user_id"],
                                   theater_detail["seat_number"], theater_detail["total_paid"],
                                   theater_detail["movie_index_id"], theater_detail["time_slot"])
