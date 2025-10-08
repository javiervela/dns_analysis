import subprocess


class DNSClient:
    def __init__(self):
        pass

    def _query(self, domain, record_type, dns_server=None, norecurse=False):
        """Query the DNS for a specific record type using dig CLI tool."""
        cmd = ["dig"]
        if dns_server:
            cmd.append(f"@{dns_server}")
        cmd += [domain, record_type, "+short"]
        if norecurse:
            cmd.append("+norecurse")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            output = result.stdout.strip()
            return output.split("\n") if output else []
        except subprocess.CalledProcessError as e:
            print(f"Error querying DNS: {e}")
            return []

    def _query_ttl(self, domain, record_type, dns_server=None, norecurse=False):
        """Query the DNS for a specific record type using dig CLI tool and return TTLs."""
        cmd = ["dig"]
        if dns_server:
            cmd.append(f"@{dns_server}")
        cmd += [domain, record_type]
        if norecurse:
            cmd.append("+norecurse")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            output = result.stdout.strip()
            ttls = []
            for line in output.split("\n"):
                if line and not line.startswith(";"):
                    parts = line.split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        ttls.append(int(parts[1]))
            return ttls
        except subprocess.CalledProcessError as e:
            print(f"Error querying DNS for TTL: {e}")
            return []

    def _reverse_lookup(self, ip_address, dns_server=None, norecurse=False):
        """Perform a reverse DNS lookup for an IP address."""
        cmd = ["dig"]
        if dns_server:
            cmd.append(f"@{dns_server}")
        cmd += ["-x", ip_address, "+short"]
        if norecurse:
            cmd.append("+norecurse")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            output = result.stdout.strip()
            return output.split("\n") if output else []
        except subprocess.CalledProcessError as e:
            print(f"Error performing reverse lookup: {e}")
            return []

    def _get_query_time(self, domain, dns_server=None, norecurse=False):
        """Get the Query Time from the dig command output."""
        cmd = ["dig"]
        if dns_server:
            cmd.append(f"@{dns_server}")
        cmd += [domain]
        if norecurse:
            cmd.append("+norecurse")
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            for line in result.stdout.strip().split("\n"):
                if "Query time:" in line:
                    parts = line.split("Query time:")[1].strip().split()
                    return int(parts[0])
            return None
        except subprocess.CalledProcessError as e:
            print(f"Error getting Query Time: {e}")
            return None

    def get_a_record(self, domain, dns_server=None, norecurse=False):
        """Get the A record for a domain."""
        return self._query(domain, "A", dns_server, norecurse)

    def get_web_record(self, domain, dns_server=None, norecurse=False):
        """Get the web (CNAME) record for a domain."""
        return self._query(f"www.{domain}", "CNAME", dns_server, norecurse)

    def get_ns_record(self, domain, dns_server=None, norecurse=False):
        """Get the NS record for a domain."""
        return self._query(domain, "NS", dns_server, norecurse)

    def get_mx_record(self, domain, dns_server=None, norecurse=False):
        """Get the MX record for a domain, returning only mail servers as a list."""
        return [
            r.split()[1]
            for r in self._query(domain, "MX", dns_server, norecurse)
            if len(r.split()) == 2
        ]

    def reverse_lookup(self, ip_address, dns_server=None, norecurse=False):
        """Perform a reverse DNS lookup for an IP address."""
        return self._reverse_lookup(ip_address, dns_server, norecurse)

    def get_query_time(self, domain, dns_server=None, norecurse=False):
        """Get the Query Time for a domain."""
        return self._get_query_time(domain, dns_server, norecurse)

    def get_attl(self, domain):
        """Get the Authoritative TTL for a domain."""
        ns_records = self.get_ns_record(domain)
        if not ns_records:
            return None
        ns = ns_records[0].rstrip(".")
        ttls = self._query_ttl(domain, "A", dns_server=ns)
        return max(ttls) if ttls else None
