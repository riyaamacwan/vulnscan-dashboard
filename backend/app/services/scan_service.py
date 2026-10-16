from app.scanner.tls_probe import check_tls
from app.scanner.rules_engine import evaluate_services, evaluate_tls
import threading
from datetime import datetime, timezone

from flask import current_app

from app.extensions import db
from app.models import Scan, Finding
from app.scanner.nmap_scanner import run_nmap_scan
from app.scanner.rules_engine import evaluate_services


def start_scan(scan_id: int, host: str, ports: str):
    app = current_app._get_current_object()

    thread = threading.Thread(
        target=_execute_scan,
        args=(app, scan_id, host, ports),
        daemon=True
    )

    thread.start()


def _execute_scan(app, scan_id: int, host: str, ports: str):
    with app.app_context():
        scan = Scan.query.get(scan_id)

        if not scan:
            return

        scan.status = "running"
        scan.started_at = datetime.now(timezone.utc)
        db.session.commit()

        try:
            nmap_result = run_nmap_scan(host, ports)
            findings = evaluate_services(nmap_result)
            tls_result = check_tls(host, 443)
            findings.extend(evaluate_tls(tls_result))
            for item in findings:
                finding = Finding(
                    scan_id=scan.id,
                    title=item["title"],
                    severity=item["severity"],
                    category=item["category"],
                    description=item["description"],
                    evidence=item["evidence"],
                    cve_ids=item["cve_ids"],
                    remediation=item["remediation"],
                )

                db.session.add(finding)

            scan.status = "completed"

        except Exception as exc:
            scan.status = "failed"
            scan.encrypted_result = str(exc).encode()

            print("SCAN ERROR:", repr(exc))

        finally:
            scan.finished_at = datetime.now(timezone.utc)
            db.session.commit()