from flask import request, make_response
from flask_restful import Resource
from models import db, Exercise
from schemas import exercise_schema, exercises_schema


class ExercisesResource(Resource):

    def get(self):
        exercises = Exercise.query.all()
        return make_response(exercises_schema.dump(exercises), 200)

    def post(self):
        data = request.get_json()

        try:
            exercise = Exercise(
                name=data["name"],
                category=data["category"],
                equipment=data["equipment"]
            )

            db.session.add(exercise)
            db.session.commit()

            return make_response(exercise_schema.dump(exercise), 201)

        except Exception as e:
            response = {"message": str(e)}
            return make_response(response, 400)


class ExerciseByID(Resource):

    def get(self, id):
        exercise = Exercise.query.filter_by(id=id).first()

        if exercise:
            return make_response(exercise_schema.dump(exercise), 200)

        response = {"status": 404, "message": "Exercise not found"}
        return make_response(response, 404)

    def patch(self, id):
        exercise = Exercise.query.filter_by(id=id).first()

        if not exercise:
            response = {"status": 404, "message": "Exercise not found"}
            return make_response(response, 404)

        data = request.get_json()

        try:
            for attr in data:
                setattr(exercise, attr, data[attr])

            db.session.commit()

            return make_response(exercise_schema.dump(exercise), 200)

        except Exception as e:
            response = {"message": str(e)}
            return make_response(response, 400)

    def delete(self, id):
        exercise = Exercise.query.filter_by(id=id).first()

        if exercise:
            db.session.delete(exercise)
            db.session.commit()

            response = {"message": "Exercise deleted successfully"}
            return make_response(response, 200)

        response = {"status": 404, "message": "Exercise not found"}
        return make_response(response, 404)