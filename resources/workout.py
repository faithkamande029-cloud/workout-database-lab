from flask import request, make_response
from flask_restful import Resource

from models import db, Workout
from schemas import workout_schema, workouts_schema


class WorkoutsResource(Resource):

    def get(self):
        workouts = Workout.query.all()
        return make_response(workouts_schema.dump(workouts), 200)

    def post(self):
        data = request.get_json()

        try:
            workout = Workout(
                date=data["date"],
                duration_minutes=data["duration_minutes"]
            )

            db.session.add(workout)
            db.session.commit()

            return make_response(workout_schema.dump(workout), 201)

        except Exception as e:
            response = {"message": str(e)}
            return make_response(response, 400)


class WorkoutByID(Resource):

    def get(self, id):
        workout = Workout.query.filter_by(id=id).first()

        if workout:
            return make_response(workout_schema.dump(workout), 200)

        response = {"status": 404, "message": "Workout not found"}
        return make_response(response, 404)

    def patch(self, id):
        workout = Workout.query.filter_by(id=id).first()

        if not workout:
            response = {"status": 404, "message": "Workout not found"}
            return make_response(response, 404)

        data = request.get_json()

        try:
            for attr in data:
                setattr(workout, attr, data[attr])

            db.session.commit()

            return make_response(workout_schema.dump(workout), 200)

        except Exception as e:
            response = {"message": str(e)}
            return make_response(response, 400)

    def delete(self, id):
        workout = Workout.query.filter_by(id=id).first()

        if workout:
            db.session.delete(workout)
            db.session.commit()

            response = {"message": "Workout deleted successfully"}
            return make_response(response, 200)

        response = {"status": 404, "message": "Workout not found"}
        return make_response(response, 404)