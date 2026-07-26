from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db
from flask_restful import Api

from resources.exercise import ExercisesResource, ExerciseByID
from resources.workout import WorkoutsResource, WorkoutByID
from resources.workout_exercise import WorkoutExerciseResource

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///workout.db"

migrate = Migrate(app=app, db=db)

db.init_app(app=app)

api = Api(app=app)

api.add_resource(ExercisesResource, "/exercises")
api.add_resource(ExerciseByID, "/exercises/<int:id>")

api.add_resource(WorkoutsResource, "/workouts")
api.add_resource(WorkoutByID, "/workouts/<int:id>")

api.add_resource(WorkoutExerciseResource,"/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")