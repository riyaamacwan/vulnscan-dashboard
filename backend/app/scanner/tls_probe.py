import ssl
import socket
from datetime import datetime, timezone

def check_tls(host: str, port: int = 443) -> dict | None:
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as secure_sock:
                cert = secure_sock.getpeercert()
                protocol = secure_sock.version()
                cipher = secure_sock.cipher()

        if not cert or "notAfter" not in cert:
            return None

        expiry = datetime.strptime(
            cert["notAfter"], "%b %d %H:%M:%S %Y %Z"
        ).replace(tzinfo=timezone.utc)

        days_left = (expiry - datetime.now(timezone.utc)).days

        return {
            "host": host,
            "port": port,
            "protocol": protocol,
            "cipher": cipher[0] if cipher else None,
            "expires_at": expiry.isoformat(),
            "days_until_expiry": days_left,
        }

    except Exception:
        return None