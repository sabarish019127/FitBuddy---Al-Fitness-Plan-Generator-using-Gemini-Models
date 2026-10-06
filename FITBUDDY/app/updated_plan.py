def fallback_plan(
    data,
    nutrition
):

    weekly_workouts = [

        (
            "Day 1 - Full Body",
            "Squats 3x10, Push-ups 3x8-12, "
            "Rows 3x10, Plank 3x30 seconds"
        ),

        (
            "Day 2 - Cardio & Core",
            "Walking or cycling 25-35 minutes, "
            "Dead bug 3x10, Plank 3x30 seconds"
        ),

        (
            "Day 3 - Lower Body",
            "Squats 3x10, Lunges 3x10 each leg, "
            "Glute bridge 3x12, Calf raises 3x15"
        ),

        (
            "Day 4 - Upper Body",
            "Push-ups 3x8-12, Rows 3x10, "
            "Shoulder press 3x10, Curls 3x12"
        ),

        (
            "Day 5 - Full Body",
            "Goblet squat 3x10, Push-ups 3x10, "
            "Rows 3x10, Mountain climbers 3x20"
        ),

        (
            "Day 6 - Active Recovery",
            "Easy walk 20-30 minutes plus "
            "10 minutes of mobility"
        ),

        (
            "Day 7 - Rest",
            "Complete rest or gentle mobility"
        )
    ]


    workout_days = data["workout_days"]


    for index in range(
        workout_days,
        7
    ):

        if index >= 0:

            weekly_workouts[index] = (

                weekly_workouts[index][0],

                "Rest or gentle mobility "
                "for recovery."
            )


    lines = [

        f"# FitBuddy Plan for {data['name']}",

        "",

        "## Overview",

        f"- Goal: "
        f"{data['goal'].replace('_', ' ').title()}",

        f"- Equipment: "
        f"{data['equipment'].replace('_', ' ')}",

        f"- Diet: {data['diet']}",

        f"- Allergies: "
        f"{data.get('allergies') or 'None'}",

        "",

        "## Daily Nutrition Target",

        f"- Calories: "
        f"{nutrition['calories']} kcal",

        f"- Protein: "
        f"{nutrition['protein_g']} g",

        f"- Carbohydrates: "
        f"{nutrition['carbs_g']} g",

        f"- Fat: "
        f"{nutrition['fat_g']} g",

        "",

        "## Weekly Workout"
    ]


    for title, details in weekly_workouts:

        lines.extend([

            f"### {title}",

            details,

            ""
        ])


    lines.extend([

        "## Meal Framework",

        "- Breakfast: oats or whole grains + "
        "fruit + a suitable protein source.",

        "- Lunch: whole grains + vegetables + "
        "a suitable protein source.",

        "- Snack: fruit + yogurt or nuts "
        "according to diet and allergies.",

        "- Dinner: vegetables + protein + "
        "moderate carbohydrates.",

        "",

        "## Hydration",

        "- Drink water regularly throughout the day.",

        "- Increase fluids during hot weather "
        "and exercise.",

        "",

        "## Recovery",

        "- Keep a consistent sleep schedule.",

        "- Take rest days seriously.",

        "- Increase training gradually.",

        "- Stop exercise if you experience "
        "sharp or unusual pain.",

        "",

        "## Progress Tracking",

        "- Record workouts.",

        "- Track body measurements periodically.",

        "- Track energy and recovery.",

        "- Review progress every few weeks.",

        "",

        "> This is general fitness information "
        "and is not medical advice."
    ])


    return "\n".join(
        lines
    )
