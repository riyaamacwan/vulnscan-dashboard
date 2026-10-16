import csv
import io

from flask import Blueprint, Response
from app.models import Scan
from app.utils.security import jwt_required
reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/<int:scan_id>/csv", methods=["GET"])
@jwt_required
def export_scan_csv(scan_id):
    scan = Scan.query.get_or_404(scan_id)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Finding ID",
        "Title",
        "Severity",
        "Category",
        "Description",
        "Evidence",
        "CVEs",
        "Remediation",
    ])

    for finding in scan.findings:
        writer.writerow([
            finding.id,
            finding.title,
            finding.severity,
            finding.category,
            finding.description,
            finding.evidence,
            finding.cve_ids,
            finding.remediation,
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=scan-{scan_id}.csv"
    )

    return response