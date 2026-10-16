from flask import Blueprint, jsonify, request
from app.models import Finding

findings_bp = Blueprint("findings", __name__)

@findings_bp.route("/findings", methods=["GET"])
def list_findings():
    severity = request.args.get("severity")
    query = Finding.query

    if severity:
        query = query.filter_by(severity=severity)

    findings = query.order_by(Finding.created_at.desc()).all()

    return jsonify([
        {
            "id": f.id,
            "scan_id": f.scan_id,
            "title": f.title,
            "severity": f.severity,
            "category": f.category,
            "description": f.description,
            "evidence": f.evidence,
            "cve_ids": f.cve_ids,
            "remediation": f.remediation,
        }
        for f in findings
    ])