from dataclasses import dataclass


@dataclass
class FitnessInput:

    name: str

    age: int

    gender: str

    height_cm: float

    weight_kg: float

    goal: str

    activity_level: str

    workout_days: int

    equipment: str

    diet: str

    allergies: str = ""


    @classmethod
    def from_form(cls, form):

        return cls(

            name=form.get(
                "name",
                ""
            ).strip(),

            age=int(
                form.get(
                    "age",
                    0
                )
            ),

            gender=form.get(
                "gender",
                ""
            ).strip(),

            height_cm=float(
                form.get(
                    "height_cm",
                    0
                )
            ),

            weight_kg=float(
                form.get(
                    "weight_kg",
                    0
                )
            ),

            goal=form.get(
                "goal",
                ""
            ).strip(),

            activity_level=form.get(
                "activity_level",
                ""
            ).strip(),

            workout_days=int(
                form.get(
                    "workout_days",
                    0
                )
            ),

            equipment=form.get(
                "equipment",
                ""
            ).strip(),

            diet=form.get(
                "diet",
                ""
            ).strip(),

            allergies=form.get(
                "allergies",
                ""
            ).strip()
        )


    def validate(self):

        if not self.name:

            raise ValueError(
                "Name is required."
            )


        if not 13 <= self.age <= 100:

            raise ValueError(
                "Age must be between 13 and 100."
            )


        if self.height_cm <= 0:

            raise ValueError(
                "Height must be greater than zero."
            )


        if self.weight_kg <= 0:

            raise ValueError(
                "Weight must be greater than zero."
            )


        if not 1 <= self.workout_days <= 7:

            raise ValueError(
                "Workout days must be between 1 and 7."
            )


        if not self.gender:

            raise ValueError(
                "Gender is required."
            )


        if not self.goal:

            raise ValueError(
                "Fitness goal is required."
            )
        