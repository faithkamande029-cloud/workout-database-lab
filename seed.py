from models import db, Exercise, Workout, WorkoutExercise
from app import app
from datetime import date

with app.app_context():

    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    exercises = [
        Exercise(name="Push Up", category="Strength", equipment=False),
        Exercise(name="Squat", category="Strength", equipment=False),
        Exercise(name="Plank", category="Core", equipment=False),
        Exercise(name="Burpee", category="Cardio", equipment=False),
        Exercise(name="Jumping Jack", category="Cardio", equipment=False),
    ]

    workouts = [
        Workout(date=date(2026, 7, 26), duration_minutes=45),
        Workout(date=date(2026, 7, 27), duration_minutes=60),
        Workout(date=date(2026, 7, 28), duration_minutes=30),
    ]

    db.session.add_all(exercises)
    db.session.add_all(workouts)
    db.session.commit()

    workout_exercises = [
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, sets=3, reps=12),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[1].id, sets=3, reps=15),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[2].id, sets=3, reps=45),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[0].id, sets=4, reps=10),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[3].id, sets=4, reps=8),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[2].id, sets=4, reps=60),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[4].id, sets=3, reps=30),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Seed data created successfully!")