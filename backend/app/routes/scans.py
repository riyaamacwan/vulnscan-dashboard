from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Target, Scan
from app.services.scan_service import start_scan

scans_bp = Blueprint("scans", __name__)

BLOCKED_HOSTS = {
    "169.254.169.254",
    "metadata.google.internal",
}

@scans_bp.route("/scans", methods=["POST"])
def create_scan():
    data = request.get_json(silent=True) or {}

    host = data.get("host", "").strip()
    ports = data.get("ports", "1-1000")
    authorized = data.get("authorized", False)

    if not host:
        return jsonify({"error": "host is required"}), 400

    if host in BLOCKED_HOSTS:
        return jsonify({"error": "this target is not allowed"}), 400

    if not authorized:
        return jsonify({"error": "you must confirm authorization"}), 400

    target = Target.query.filter_by(host=host).first()

    if not target:
        target = Target(name=host, host=host, authorized=True)
        db.session.add(target)
        db.session.commit()

    scan = Scan(target_id=target.id, status="queued")
    db.session.add(scan)
    db.session.commit()

    start_scan(scan.id, host, ports)

    return jsonify({
        "scan_id": scan.id,
        "status": scan.status
    }), 202


@scans_bp.route("/scans/<int:scan_id>", methods=["GET"])
def get_scan(scan_id):
    scan = Scan.query.get_or_404(scan_id)

    return jsonify({
        "id": scan.id,
        "status": scan.status,
        "target": scan.target.host,
        "started_at": scan.started_at,
        "finished_at": scan.finished_at,
        "findings": [
            {
                "id": finding.id,
                "title": finding.title,
                "severity": finding.severity,
                "category": finding.category,
                "description": finding.description,
                "evidence": finding.evidence,
                "cve_ids": finding.cve_ids,
                "remediation": finding.remediation,
            }
            for finding in scan.findings
        ],
    })