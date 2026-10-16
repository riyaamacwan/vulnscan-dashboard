from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Finding
from app.utils.security import jwt_required

findings_bp = Blueprint("findings", __name__)


@findings_bp.route("/findings", methods=["GET"])
@jwt_required
def list_findings():
    severity = request.args.get("severity")
    category = request.args.get("category")
    scan_id = request.args.get("scan_id", type=int)

    query = Finding.query

    if severity:
        query = query.filter(Finding.severity == severity.lower())

    if category:
        query = query.filter(Finding.category == category.lower())

    if scan_id:
        query = query.filter(Finding.scan_id == scan_id)

    findings = query.order_by(Finding.created_at.desc()).all()

    return jsonify([
        {
            "id": finding.id,
            "scan_id": finding.scan_id,
            "title": finding.title,
            "severity": finding.severity,
            "category": finding.category,
            "description": finding.description,
            "evidence": finding.evidence,
            "cve_ids": finding.cve_ids,
            "remediation": finding.remediation,
            "created_at": finding.created_at.isoformat()
            if finding.created_at else None,
        }
        for finding in findings
    ])


@findings_bp.route("/findings/<int:finding_id>", methods=["GET"])
@jwt_required
def get_finding(finding_id):
    finding = Finding.query.get_or_404(finding_id)

    return jsonify({
        "id": finding.id,
        "scan_id": finding.scan_id,
        "title": finding.title,
        "severity": finding.severity,
        "category": finding.category,
        "description": finding.description,
        "evidence": finding.evidence,
        "cve_ids": finding.cve_ids,
        "remediation": finding.remediation,
        "created_at": finding.created_at.isoformat()
        if finding.created_at else None,
    })