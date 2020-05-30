from Database.Connection import Connection
import jwt
import uuid
from datetime import datetime
from flask import jsonify
from bson import ObjectId


class TheaterModel:
    def __init__(self):
        self.__theater_collection = Connection.connect("theater")
        self.__movie_collection = Connection.connect("movie_index")
        self.__booked_movie_collection = Connection.connect(
            "booked_movie_ticket")

    def add_theater(self, theater_name, address):
        result = self.__theater_collection.count_documents(
            {"theater_name": theater_name})
        if result == 0:
            result = self.__theater_collection.insert_one(
                {"theater_name": theater_name, "address": address, "movies": [],
                 "added_datetime": datetime.utcnow()})
            if result.inserted_id:
                return jsonify({"theater_id": str(result.inserted_id)}), 200
            else:
                return jsonify({"error": "Fail to add theater"}), 400
        else:
            return jsonify({"warning": "Theater detail already exists"}), 400

    def add_movie(self, theater_id, movie_name, total_seat, time_slot):
        result = self.__theater_collection.count_documents({"_id": ObjectId(theater_id),
                                                            "movies.movie_name": movie_name})
        if result == 0:
            movie_id = uuid.uuid4()
            result = self.__theater_collection.update_one({"_id": ObjectId(theater_id)},
                                                          {"$push": {"movies": {"movie_id": movie_id,
                                                                                "movie_name": movie_name,
                                                                                "total_seat": total_seat,
                                                                                "time_slot": time_slot,
                                                                                "added_datetime": datetime.utcnow()}}})
            if result.modified_count:
                return jsonify({"Message": result.modified_count, "movie_id": movie_id}), 200
            else:
                return jsonify({"Message": result.modified_count, "error": "Fail to add movie"}), 400
        else:
            return jsonify({"warning": "Movie detail already exists"}), 400

    def seat_availability(self, theater_id, movie_id, time_slot):
        seats = []
        result_movie = self.__movie_collection.find({"theater_id": theater_id, "movie_id": movie_id,
                                                     "time_slot": time_slot},
                                                    {"seat_number": 1, "_id": 0})
        result_booked = self.__booked_movie_collection.find(
            {"theater_id": theater_id, "movie_id": movie_id, "time_slot": time_slot},
            {"seat_number": 1, "_id": 0})
        if result_movie is not None:
            for result in result_movie:
                seats.extend(result["seat_number"])
        if result_booked is not None:
            for result in result_booked:
                seats.extend(result["seat_number"])

        available_seats = list(
            filter(lambda seat: seat not in seats, range(1, 41)))

        return {"Seats": available_seats}

    def book_seat(self, theater_id, movie_id, user_id, seat_number, time_slot):

        available_seats = self.seat_availability(
            theater_id, movie_id, time_slot)["Seats"]
        if len(set(available_seats).intersection(set(seat_number))) != len(seat_number):
            return jsonify({"warning": "Seats already booked", "available_seats": available_seats})

        result = self.__movie_collection.insert_one({"theater_id": theater_id,
                                                     "movie_id": movie_id,
                                                     "user_id": user_id,
                                                     "seat_number": seat_number,
                                                     "time_slot": time_slot,
                                                     "createdAt": datetime.utcnow()
                                                     })

        if result.inserted_id:
            return jsonify({"theater_id": theater_id,
                            "movie_id": movie_id,
                            "seat_number": seat_number,
                            "time_slot": time_slot,
                            "message": "Pay within 30 seconds",
                            "movie_index_id": str(result.inserted_id)
                            }), 200
        else:
            return jsonify({"error": "Fail to reserve seats"}), 400

    def payment_process(self, theater_id, movie_id, user_id, seat_number, total_paid, movie_index_id, time_slot):

        result = self.__movie_collection.delete_one(
            {"_id": ObjectId(movie_index_id)})
        if result.deleted_count:
            result = self.__booked_movie_collection.insert_one({"theater_id": theater_id,
                                                                "movie_id": movie_id,
                                                                "user_id": user_id,
                                                                "seat_number": seat_number,
                                                                "amount_paid": total_paid,
                                                                "time_slot": time_slot,
                                                                "booked_datetime": datetime.utcnow()
                                                                })

            if result.inserted_id:
                return jsonify({"theater_id": theater_id,
                                "movie_id": movie_id,
                                "user_id": user_id,
                                "seat_number": seat_number,
                                "time_slot": time_slot,
                                "amount_paid": total_paid
                                }), 200
            else:
                return jsonify({"error": "Fail to book seats"}), 400
        else:
            return jsonify({"error": "Session Timeout"}), 400
