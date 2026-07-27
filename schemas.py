from marshmallow import Schema, fields, ValidationError, validates_schema

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment = fields.Bool(required=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        errors = {}

        if "name" in data and len(data["name"].strip()) == 0:
            errors["name"] = ["Exercise name is required."]

        valid_categories = ["Strength", "Cardio", "Core", "Flexibility"]

        if "category" in data and data["category"] not in valid_categories:
            errors["category"] = [
                f"Category must be one of: {', '.join(valid_categories)}."
            ]

        if errors:
            raise ValidationError(errors)
        

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

    @validates_schema
    def validate_schema(self, data, **kwargs):
        errors = {}

        if data.get("reps") is None and data.get("duration_seconds") is None:
            errors["reps"] = [
                "Provide either reps or duration_seconds."
            ]

        if errors:
            raise ValidationError(errors)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        errors = {}

        if "duration_minutes" in data:
            if data["duration_minutes"] <= 0:
                errors["duration_minutes"] = [
                    "Duration must be greater than 0 minutes."
                ]

        if errors:
            raise ValidationError(errors)

# Exercise schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

# Workout schemas
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

# WorkoutExercise schemas
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)