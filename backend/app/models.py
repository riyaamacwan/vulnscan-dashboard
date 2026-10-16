from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Target(db.Model):
    __tablename__ = "targets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    host = db.Column(db.String(255), unique=True, nullable=False)
    authorized = db.Column(db.Boolean, default=False, nullable=False)

    scans = db.relationship(
        "Scan",
        backref="target",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Scan(db.Model):
    __tablename__ = "scans"

    id = db.Column(db.Integer, primary_key=True)

    target_id = db.Column(
        db.Integer,
        db.ForeignKey("targets.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="queued",
        nullable=False
    )

    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)

    encrypted_result = db.Column(
        db.LargeBinary,
        nullable=True
    )

    findings = db.relationship(
        "Finding",
        backref="scan",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Finding(db.Model):
    __tablename__ = "findings"

    id = db.Column(db.Integer, primary_key=True)

    scan_id = db.Column(
        db.Integer,
        db.ForeignKey("scans.id"),
        nullable=False
    )

    title = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    description = db.Column(
        db.Text,
        nullable=True
    )

    evidence = db.Column(
        db.Text,
        nullable=True
    )

    cve_ids = db.Column(
        db.Text,
        nullable=True
    )

    remediation = db.Column(
        db.Text,
        nullable=True
    )