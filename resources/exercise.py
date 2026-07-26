from flask import request, make_response
from flask_restful import Resource
from marshmallow import ValidationError

from models import db, Exercise
from schemas import exercise_schema, exercises_schema


class ExercisesResource(Resource):

    def get(self):
        exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(exercises), 200)

    def post(self):
        try:
            data = exercise_schema.load(request.get_json())

            exercise = Exercise(**data)

            db.session.add(exercise)
            db.session.commit()

            return make_response(exercise_schema.dump(exercise), 201)

        except ValidationError as err:
            return make_response(err.messages, 400)


class ExerciseByID(Resource):

    def get(self, id):
        exercise = Exercise.query.filter_by(id=id).first()

        if exercise:
            return make_response(exercise_schema.dump(exercise), 200)

        return make_response(
            {"status": 404, "message": "Exercise not found"},
            404
        )

    def patch(self, id):
        exercise = Exercise.query.filter_by(id=id).first()

        if not exercise:
            return make_response(
                {"status": 404, "message": "Exercise not found"},
                404
            )

        try:
            data = exercise_schema.load(request.get_json(), partial=True)

            for key, value in data.items():
                setattr(exercise, key, value)

            db.session.commit()

            return make_response(exercise_schema.dump(exercise), 200)

        except ValidationError as err:
            return make_response(err.messages, 400)

    def delete(self, id):
        exercise = Exercise.query.filter_by(id=id).first()

        if exercise:
            db.session.delete(exercise)
            db.session.commit()

            return make_response(
                {"message": "Exercise deleted successfully"},
                200
            )

        return make_response(
            {"status": 404, "message": "Exercise not found"},
            404
        )