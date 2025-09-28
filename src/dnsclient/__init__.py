import subprocess


class DNSClient:
    def __init__(self):
        pass

    def _query(self, domain, record_type, dns_server=None):
        """Query the DNS for a specific record type using dig CLI tool."""
        cmd = ["dig"]
        if dns_server:
            cmd.append(f"@{dns_server}")
        cmd += [domain, record_type, "+short"]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n")
        except subprocess.CalledProcessError as e:
            print(f"Error querying DNS: {e}")
            return []

    def _reverse_lookup(self, ip_address, dns_server=None):
        """Perform a reverse DNS lookup for an IP address."""
        cmd = ["dig"]
        if dns_server:
            cmd.append(f"@{dns_server}")
        cmd += ["-x", ip_address, "+short"]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n")
        except subprocess.CalledProcessError as e:
            print(f"Error performing reverse lookup: {e}")
            return []

    def get_a_record(self, domain, dns_server=None):
        """Get the A record for a domain."""
        return self._query(domain, "A", dns_server)

    def get_web_record(self, domain, dns_server=None):
        """Get the web (CNAME) record for a domain."""
        return self._query(f"www.{domain}", "CNAME", dns_server)

    def get_ns_record(self, domain, dns_server=None):
        """Get the NS record for a domain."""
        return self._query(domain, "NS", dns_server)

    def get_mx_record(self, domain, dns_server=None):
        """Get the MX record for a domain, returning only mail servers as a list."""
        return [
            r.split()[1]
            for r in self._query(domain, "MX", dns_server)
            if len(r.split()) == 2
        ]

    def reverse_lookup(self, ip_address, dns_server=None):
        """Perform a reverse DNS lookup for an IP address."""
        return self._reverse_lookup(ip_address, dns_server)
