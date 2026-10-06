import os

from google import genai


def build_prompt(
    data,
    nutrition
):

    return f"""
You are FitBuddy, an AI fitness-plan assistant.

Create a practical personalized 7-day fitness
and nutrition plan.

USER INFORMATION

Name:
{data["name"]}

Age:
{data["age"]}

Gender:
{data["gender"]}

Height:
{data["height_cm"]} cm

Weight:
{data["weight_kg"]} kg

Goal:
{data["goal"]}

Activity level:
{data["activity_level"]}

Workout days per week:
{data["workout_days"]}

Equipment:
{data["equipment"]}

Diet:
{data["diet"]}

Allergies or intolerances:
{data.get("allergies") or "None"}


ESTIMATED DAILY NUTRITION

Calories:
{nutrition["calories"]} kcal

Protein:
{nutrition["protein_g"]} g

Carbohydrates:
{nutrition["carbs_g"]} g

Fat:
{nutrition["fat_g"]} g


RETURN THE PLAN IN MARKDOWN.

Include:

1. Fitness plan overview

2. Seven-day workout schedule

3. Exercises

4. Sets and repetitions

5. Rest periods

6. Seven-day meal suggestions

7. Breakfast

8. Lunch

9. Dinner

10. Snacks

11. Hydration recommendations

12. Recovery recommendations

13. Progress tracking


IMPORTANT:

Respect the user's equipment.

Respect the user's diet.

Respect allergies and intolerances.

Do not recommend foods listed as allergies.

Do not diagnose diseases.

Do not provide medical treatment.

If the user is under 18, keep the plan conservative
and recommend adult/professional supervision.

Make the plan realistic and easy to understand.
"""


def generate_with_gemini(
    data,
    nutrition
):

    api_key = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()


    if not api_key:

        return None


    client = genai.Client(
        api_key=api_key
    )


    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )


    response = client.models.generate_content(

        model=model,

        contents=build_prompt(
            data,
            nutrition
        )
    )


    return getattr(
        response,
        "text",
        None
    )
