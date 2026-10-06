def calculate_bmi(
    height_cm,
    weight_kg
):

    height_m = height_cm / 100

    bmi = weight_kg / (
        height_m * height_m
    )

    return round(
        bmi,
        1
    )


def bmi_category(bmi):

    if bmi < 18.5:

        return "Underweight"

    elif bmi < 25:

        return "Healthy range"

    elif bmi < 30:

        return "Overweight"

    else:

        return "Obesity range"


def estimate_nutrition(
    age,
    gender,
    height_cm,
    weight_kg,
    activity_level,
    goal
):

    gender_lower = gender.lower()

    if gender_lower == "male":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    elif gender_lower == "female":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    else:

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 78
        )


    activity_factors = {

        "sedentary": 1.20,

        "light": 1.375,

        "moderate": 1.55,

        "very_active": 1.725
    }


    activity_factor = activity_factors.get(
        activity_level,
        1.375
    )


    tdee = bmr * activity_factor


    if goal == "fat_loss":

        calories = tdee - 400

    elif goal == "muscle_gain":

        calories = tdee + 250

    else:

        calories = tdee


    calories = max(
        1200,
        round(calories)
    )


    if goal == "muscle_gain":

        protein = round(
            weight_kg * 1.8
        )

    else:

        protein = round(
            weight_kg * 1.6
        )


    fat = round(
        calories * 0.25 / 9
    )


    carbs = round(
        (
            calories
            - protein * 4
            - fat * 9
        ) / 4
    )


    return {

        "calories": calories,

        "protein_g": max(
            1,
            protein
        ),

        "carbs_g": max(
            1,
            carbs
        ),

        "fat_g": max(
            1,
            fat
        )
    }
