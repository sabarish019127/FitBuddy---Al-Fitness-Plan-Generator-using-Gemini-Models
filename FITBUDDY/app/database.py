import sqlite3

from flask import current_app, g


# ============================================================
# DATABASE SCHEMA
# ============================================================

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    age INTEGER NOT NULL,

    gender TEXT NOT NULL,

    height_cm REAL NOT NULL,

    weight_kg REAL NOT NULL,

    goal TEXT NOT NULL,

    activity_level TEXT NOT NULL,

    workout_days INTEGER NOT NULL,

    equipment TEXT NOT NULL,

    diet TEXT NOT NULL,

    allergies TEXT DEFAULT '',

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS fitness_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    plan_text TEXT NOT NULL,

    calories INTEGER,

    protein_g INTEGER,

    carbs_g INTEGER,

    fat_g INTEGER,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
"""


# ============================================================
# GET DATABASE CONNECTION
# ============================================================

def get_db():
    """
    Get a SQLite connection for the current Flask request.

    Flask's `g` object stores the connection only for the
    current application/request context. This prevents one
    request thread from accidentally reusing a SQLite
    connection created by another thread.
    """

    if "db" not in g:

        g.db = sqlite3.connect(
            current_app.config["DATABASE"]
        )

        # Return rows that can be accessed by column name.
        g.db.row_factory = sqlite3.Row

        # Enable foreign-key support.
        g.db.execute(
            "PRAGMA foreign_keys = ON"
        )

    return g.db


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

def close_db(exception=None):
    """
    Close the database connection at the end of the
    Flask application context.
    """

    db = g.pop("db", None)

    if db is not None:
        db.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_db():
    """
    Create the database tables if they don't already exist.
    """

    database_path = current_app.config["DATABASE"]

    connection = sqlite3.connect(
        database_path
    )

    try:

        # Enable foreign keys.
        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        # Create tables.
        connection.executescript(
            SCHEMA
        )

        # Save changes.
        connection.commit()

    finally:

        # Always close this temporary initialization connection.
        connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(data):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO users
        (
            name,
            age,
            gender,
            height_cm,
            weight_kg,
            goal,
            activity_level,
            workout_days,
            equipment,
            diet,
            allergies
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data["name"],
            data["age"],
            data["gender"],
            data["height_cm"],
            data["weight_kg"],
            data["goal"],
            data["activity_level"],
            data["workout_days"],
            data["equipment"],
            data["diet"],
            data.get("allergies", "")
        )
    )

    db.commit()

    return cursor.lastrowid


# ============================================================
# CREATE FITNESS PLAN
# ============================================================

def create_plan(user_id, plan, nutrition):

    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO fitness_plans
        (
            user_id,
            plan_text,
            calories,
            protein_g,
            carbs_g,
            fat_g
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            plan,
            nutrition["calories"],
            nutrition["protein_g"],
            nutrition["carbs_g"],
            nutrition["fat_g"]
        )
    )

    db.commit()

    return cursor.lastrowid


# ============================================================
# GET SINGLE FITNESS PLAN
# ============================================================

def get_plan(plan_id):

    db = get_db()

    return db.execute(
        """
        SELECT
            p.*,

            u.name,
            u.goal,
            u.age,
            u.gender,
            u.height_cm,
            u.weight_kg,
            u.activity_level,
            u.workout_days,
            u.equipment,
            u.diet,
            u.allergies

        FROM fitness_plans p

        JOIN users u
            ON u.id = p.user_id

        WHERE p.id = ?
        """,
        (plan_id,)
    ).fetchone()


# ============================================================
# GET ALL USERS
# ============================================================

def get_all_users():

    db = get_db()

    return db.execute(
        """
        SELECT
            u.*,

            p.id AS plan_id

        FROM users u

        LEFT JOIN fitness_plans p

            ON p.id = (
                SELECT id

                FROM fitness_plans

                WHERE user_id = u.id

                ORDER BY id DESC

                LIMIT 1
            )

        ORDER BY u.id DESC
        """
    ).fetchall()
