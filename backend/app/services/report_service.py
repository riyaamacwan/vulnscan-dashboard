import csv
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_csv(scan) -> io.BytesIO:
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Finding ID", "Title", "Severity", "Category",
        "Description", "Evidence", "CVEs", "Remediation"
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

    output.seek(0)
    return io.BytesIO(output.getvalue().encode("utf-8"))


def generate_pdf(scan) -> io.BytesIO:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Vulnerability Scan Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"<b>Scan ID:</b> {scan.id}<br/>"
        f"<b>Target:</b> {scan.target.host}<br/>"
        f"<b>Status:</b> {scan.status}<br/>"
        f"<b>Started:</b> {scan.started_at}<br/>"
        f"<b>Finished:</b> {scan.finished_at}",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 20))

    data = [["Title", "Severity", "Category", "CVEs"]]

    for finding in scan.findings:
        data.append([
            finding.title,
            finding.severity,
            finding.category,
            finding.cve_ids or "-",
        ])

    table = Table(data, colWidths=[220, 70, 90, 120])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)

    return buffer