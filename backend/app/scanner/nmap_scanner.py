import nmap

def run_nmap_scan(target: str, ports: str = "1-1000") -> dict:
    nm = nmap.PortScanner()
    nm.scan(hosts=target, ports=ports, arguments="-sV --version-light -T3")

    result = {"hosts": []}

    for host in nm.all_hosts():
        host_data = {
            "host": host,
            "state": nm[host].state(),
            "services": []
        }

        for protocol in nm[host].all_protocols():
            for port in nm[host][protocol].keys():
                service = nm[host][protocol][port]
                host_data["services"].append({
                    "port": port,
                    "protocol": protocol,
                    "state": service.get("state"),
                    "name": service.get("name"),
                    "product": service.get("product"),
                    "version": service.get("version"),
                    "extrainfo": service.get("extrainfo"),
                })

        result["hosts"].append(host_data)

    return result