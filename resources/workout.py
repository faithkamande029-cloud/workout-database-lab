from flask import request, make_response
from flask_restful import Resource
from marshmallow import ValidationError

from models import db, Workout
from schemas import workout_schema, workouts_schema


class WorkoutsResource(Resource):

    def get(self):
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)

    def post(self):
        try:
            data = workout_schema.load(request.get_json())

            workout = Workout(**data)

            db.session.add(workout)
            db.session.commit()

            return make_response(workout_schema.dump(workout), 201)

        except ValidationError as err:
            return make_response(err.messages, 400)


class WorkoutByID(Resource):

    def get(self, id):
        workout = Workout.query.filter_by(id=id).first()

        if workout:
            return make_response(workout_schema.dump(workout), 200)

        return make_response(
            {"status": 404, "message": "Workout not found"},
            404
        )

    def patch(self, id):
        workout = Workout.query.filter_by(id=id).first()

        if not workout:
            return make_response(
                {"status": 404, "message": "Workout not found"},
                404
            )

        try:
            data = workout_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(workout, key, value)

            db.session.commit()

            return make_response(workout_schema.dump(workout), 200)

        except ValidationError as err:
            return make_response(err.messages, 400)

    def delete(self, id):
        workout = Workout.query.filter_by(id=id).first()

        if workout:
            db.session.delete(workout)
            db.session.commit()

            return make_response(
                {"message": "Workout deleted successfully"},
                200
            )

        return make_response(
            {"status": 404, "message": "Workout not found"},
            404
        )