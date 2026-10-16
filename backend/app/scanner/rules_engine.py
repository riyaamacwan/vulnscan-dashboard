RULES = [
    {
        "id": "OPEN_TELNET",
        "title": "Telnet service exposed",
        "severity": "high",
        "category": "service",
        "description": "Telnet transmits credentials and traffic without encryption.",
        "remediation": "Disable Telnet and use SSH with key-based authentication.",
        "cves": [],
        "match": lambda service: (
            service.get("name") == "telnet"
            and service.get("state") == "open"
        ),
    },
    {
        "id": "FTP_SERVICE",
        "title": "FTP service exposed",
        "severity": "medium",
        "category": "service",
        "description": "An FTP service was detected. FTP may expose credentials in plaintext.",
        "remediation": "Restrict FTP access, use SFTP where possible, and keep the service patched.",
        "cves": [],
        "match": lambda service: (
            service.get("name") == "ftp"
            and service.get("state") == "open"
        ),
    },
]

def evaluate_services(nmap_result: dict) -> list[dict]:
    findings = []

    for host in nmap_result.get("hosts", []):
        for service in host.get("services", []):
            for rule in RULES:
                try:
                    if rule["match"](service):
                        findings.append({
                            "title": rule["title"],
                            "severity": rule["severity"],
                            "category": rule["category"],
                            "description": rule["description"],
                            "evidence": (
                                f"{host['host']}:{service['port']} "
                                f"({service.get('name')})"
                            ),
                            "cve_ids": ",".join(rule["cves"]),
                            "remediation": rule["remediation"],
                        })
                except Exception:
                    continue

    return findings