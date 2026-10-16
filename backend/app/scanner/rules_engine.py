def evaluate_services(nmap_result: dict) -> list[dict]:
    """
    Evaluate Nmap service information and generate
    basic security findings.
    """

    findings = []

    for host_data in nmap_result.get("hosts", []):
        host = host_data.get("host")

        for service in host_data.get("services", []):
            port = service.get("port")
            protocol = service.get("protocol")
            state = service.get("state")
            name = service.get("name") or ""
            product = service.get("product") or ""
            version = service.get("version") or ""
            extrainfo = service.get("extrainfo") or ""

            # Only evaluate open services
            if state != "open":
                continue

            # -------------------------------------------------
            # FTP
            # -------------------------------------------------
            if port == 21 or name.lower() == "ftp":
                findings.append({
                    "title": "FTP service exposed",
                    "severity": "medium",
                    "category": "network-service",
                    "description": (
                        "An FTP service is exposed. FTP normally transmits "
                        "credentials and data without encryption."
                    ),
                    "evidence": (
                        f"{host}:{port}/{protocol} - "
                        f"{name} {product} {version}".strip()
                    ),
                    "cve_ids": "",
                    "remediation": (
                        "Disable FTP if it is not required. "
                        "Prefer SFTP or another encrypted file-transfer protocol."
                    ),
                })

            # -------------------------------------------------
            # Telnet
            # -------------------------------------------------
            if port == 23 or name.lower() == "telnet":
                findings.append({
                    "title": "Telnet service exposed",
                    "severity": "high",
                    "category": "network-service",
                    "description": (
                        "Telnet is an unencrypted remote-access protocol "
                        "and can expose credentials and session data."
                    ),
                    "evidence": (
                        f"{host}:{port}/{protocol} - "
                        f"{name} {product} {version}".strip()
                    ),
                    "cve_ids": "",
                    "remediation": (
                        "Disable Telnet and use SSH for secure remote administration."
                    ),
                })

            # -------------------------------------------------
            # HTTP
            # -------------------------------------------------
            if port == 80 or name.lower() in ("http", "http-proxy"):
                findings.append({
                    "title": "HTTP service exposed",
                    "severity": "low",
                    "category": "web-service",
                    "description": (
                        "An HTTP service is exposed without TLS encryption."
                    ),
                    "evidence": (
                        f"{host}:{port}/{protocol} - "
                        f"{name} {product} {version}".strip()
                    ),
                    "cve_ids": "",
                    "remediation": (
                        "Use HTTPS and redirect HTTP traffic to HTTPS where appropriate."
                    ),
                })

            # -------------------------------------------------
            # SMB
            # -------------------------------------------------
            if port in (139, 445) or name.lower() in ("netbios-ssn", "microsoft-ds"):
                findings.append({
                    "title": "SMB service exposed",
                    "severity": "medium",
                    "category": "network-service",
                    "description": (
                        "An SMB service is exposed. SMB should be restricted "
                        "to trusted networks and protected hosts."
                    ),
                    "evidence": (
                        f"{host}:{port}/{protocol} - "
                        f"{name} {product} {version}".strip()
                    ),
                    "cve_ids": "",
                    "remediation": (
                        "Restrict SMB access with firewall rules and disable "
                        "SMBv1. Keep the SMB implementation patched."
                    ),
                })

            # -------------------------------------------------
            # SSH
            # -------------------------------------------------
            if port == 22 or name.lower() == "ssh":
                # Informational finding rather than declaring SSH vulnerable.
                findings.append({
                    "title": "SSH service detected",
                    "severity": "info",
                    "category": "network-service",
                    "description": (
                        "An SSH service is exposed. Verify that it uses "
                        "strong authentication and current cryptographic settings."
                    ),
                    "evidence": (
                        f"{host}:{port}/{protocol} - "
                        f"{name} {product} {version}".strip()
                    ),
                    "cve_ids": "",
                    "remediation": (
                        "Keep SSH patched, disable password authentication when "
                        "appropriate, and restrict access to trusted networks."
                    ),
                })

            # -------------------------------------------------
            # Potentially outdated software
            # -------------------------------------------------
            if product and version:
                findings.append({
                    "title": "Service version detected",
                    "severity": "info",
                    "category": "service-enumeration",
                    "description": (
                        f"Nmap identified {product} version {version}. "
                        "Verify that this version is supported and patched."
                    ),
                    "evidence": (
                        f"{host}:{port}/{protocol} - "
                        f"{product} {version} {extrainfo}".strip()
                    ),
                    "cve_ids": "",
                    "remediation": (
                        "Check the vendor's security advisories and update "
                        "the service to a supported version."
                    ),
                })

    return findings


def evaluate_tls(tls_result: dict | None) -> list[dict]:
    if not tls_result:
        return []

    findings = []

    if tls_result["days_until_expiry"] < 30:
        findings.append({
            "title": "TLS certificate expiring soon",
            "severity": "medium",
            "category": "tls",
            "description": (
                f"The TLS certificate expires in "
                f"{tls_result['days_until_expiry']} days."
            ),
            "evidence": (
                f"{tls_result['host']}:{tls_result['port']} expires at "
                f"{tls_result['expires_at']}"
            ),
            "cve_ids": "",
            "remediation": (
                "Renew the TLS certificate and automate renewal."
            ),
        })

    if tls_result["protocol"] in ("TLSv1", "TLSv1.1"):
        findings.append({
            "title": "Outdated TLS protocol detected",
            "severity": "high",
            "category": "tls",
            "description": (
                f"The service supports {tls_result['protocol']}, "
                "which is deprecated and considered insecure."
            ),
            "evidence": (
                f"{tls_result['host']}:{tls_result['port']} uses "
                f"{tls_result['protocol']}"
            ),
            "cve_ids": "",
            "remediation": (
                "Disable TLS 1.0 and TLS 1.1; use TLS 1.2 or TLS 1.3."
            ),
        })

    return findings