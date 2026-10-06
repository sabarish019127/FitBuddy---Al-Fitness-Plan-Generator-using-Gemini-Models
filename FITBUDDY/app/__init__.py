from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv(
        "FLASK_SECRET_KEY",
        "fitbuddy-development-secret"
    )

    app.config["DATABASE"] = str(
        Path(app.root_path).parent / "fitbuddy.db"
    )

    from .routes import main_bp
    app.register_blueprint(main_bp)

    from .database import init_db

    with app.app_context():
        init_db()

    return app
