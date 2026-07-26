from flask import request, make_response
from flask_restful import Resource

from models import db, WorkoutExercise
from schemas import workout_exercise_schema


class WorkoutExerciseResource(Resource):

    def post(self, workout_id, exercise_id):
        data = request.get_json()

        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get("reps"),
            sets=data.get("sets"),
            duration_seconds=data.get("duration_seconds")
        )

        db.session.add(workout_exercise)
        db.session.commit()

        return make_response(
            workout_exercise_schema.dump(workout_exercise),
            201
        )