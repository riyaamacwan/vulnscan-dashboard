import os
from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.extensions import db, cors
from app.models import Target, Scan, Finding
from app.routes.scans import scans_bp
from app.routes.findings import findings_bp

load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app, origins=app.config["CORS_ORIGINS"])

    app.register_blueprint(scans_bp, url_prefix="/api")
    app.register_blueprint(findings_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app