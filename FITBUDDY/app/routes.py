from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash
)


from .schemas import FitnessInput

from .nutrition import (
    calculate_bmi,
    bmi_category,
    estimate_nutrition
)

from .database import (
    create_user,
    create_plan,
    get_plan,
    get_all_users
)

from .gemini_generator import (
    generate_with_gemini
)

from .updated_plan import (
    fallback_plan
)


main_bp = Blueprint(
    "main",
    __name__
)


def generate_plan(data):

    nutrition = estimate_nutrition(

        data["age"],

        data["gender"],

        data["height_cm"],

        data["weight_kg"],

        data["activity_level"],

        data["goal"]
    )


    try:

        plan = generate_with_gemini(
            data,
            nutrition
        )

    except Exception:

        plan = None


    if not plan:

        plan = fallback_plan(
            data,
            nutrition
        )


    return (
        plan,
        nutrition
    )


@main_bp.get("/")
def index():

    return render_template(
        "index.html"
    )


@main_bp.post("/generate")
def generate():

    try:

        data = FitnessInput.from_form(
            request.form
        )


        data.validate()


        values = data.__dict__


        plan, nutrition = generate_plan(
            values
        )


        user_id = create_user(
            values
        )


        plan_id = create_plan(

            user_id,

            plan,

            nutrition
        )


        return redirect(
            url_for(
                "main.result",
                plan_id=plan_id
            )
        )


    except (
        ValueError,
        TypeError
    ) as error:

        flash(
            str(error),
            "error"
        )


        return redirect(
            url_for(
                "main.index"
            )
        )


@main_bp.get("/result/<int:plan_id>")
def result(
    plan_id
):

    plan = get_plan(
        plan_id
    )


    if plan is None:

        return (
            "Fitness plan not found.",
            404
        )


    bmi = calculate_bmi(

        plan["height_cm"],

        plan["weight_kg"]
    )


    return render_template(

        "result.html",

        plan=plan,

        bmi=bmi,

        bmi_label=bmi_category(
            bmi
        )
    )


@main_bp.get("/users")
def all_users():

    users = get_all_users()


    return render_template(

        "all_users.html",

        users=users
    )


@main_bp.get("/api/health")
def health():

    return jsonify({

        "status": "healthy",

        "app": "FitBuddy",

        "version": "1.0.0"
    })


@main_bp.post("/api/generate")
def api_generate():

    payload = request.get_json(
        silent=True
    ) or {}


    required_fields = [

        "name",

        "age",

        "gender",

        "height_cm",

        "weight_kg",

        "goal",

        "activity_level",

        "workout_days",

        "equipment",

        "diet"
    ]


    missing = [

        field

        for field in required_fields

        if field not in payload
    ]


    if missing:

        return jsonify({

            "success": False,

            "error":
                f"Missing fields: {missing}"

        }), 400


    try:

        data = FitnessInput(

            name=str(
                payload["name"]
            ),

            age=int(
                payload["age"]
            ),

            gender=str(
                payload["gender"]
            ),

            height_cm=float(
                payload["height_cm"]
            ),

            weight_kg=float(
                payload["weight_kg"]
            ),

            goal=str(
                payload["goal"]
            ),

            activity_level=str(
                payload["activity_level"]
            ),

            workout_days=int(
                payload["workout_days"]
            ),

            equipment=str(
                payload["equipment"]
            ),

            diet=str(
                payload["diet"]
            ),

            allergies=str(
                payload.get(
                    "allergies",
                    ""
                )
            )
        )


        data.validate()


        values = data.__dict__


        plan, nutrition = generate_plan(
            values
        )


        user_id = create_user(
            values
        )


        plan_id = create_plan(

            user_id,

            plan,

            nutrition
        )


        return jsonify({

            "success": True,

            "user_id": user_id,

            "plan_id": plan_id,

            "nutrition": nutrition,

            "plan": plan
        })


    except Exception as error:

        return jsonify({

            "success": False,

            "error": str(error)

        }), 400
    