import subprocess


class DNSClient:
    def __init__(self):
        pass

    def _query(self, domain, record_type):
        """Query the DNS for a specific record type using dig CLI tool."""
        try:
            result = subprocess.run(
                ["dig", domain, record_type, "+short"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n")
        except subprocess.CalledProcessError as e:
            print(f"Error querying DNS: {e}")
            return []

    def _reverse_lookup(self, ip_address):
        """Perform a reverse DNS lookup for an IP address."""
        try:
            result = subprocess.run(
                ["dig", "-x", ip_address, "+short"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n")
        except subprocess.CalledProcessError as e:
            print(f"Error performing reverse lookup: {e}")
            return []

    def get_a_record(self, domain):
        """Get the A record for a domain."""
        return self._query(domain, "A")

    def get_web_record(self, domain):
        """Get the web (CNAME) record for a domain."""
        return self._query(f"www.{domain}", "CNAME")

    def get_ns_record(self, domain):
        """Get the NS record for a domain."""
        return self._query(domain, "NS")

    def get_mx_record(self, domain):
        """Get the MX record for a domain, returning only mail servers as a list."""
        return [r.split()[1] for r in self._query(domain, "MX") if len(r.split()) == 2]

    def reverse_lookup(self, ip_address):
        """Perform a reverse DNS lookup for an IP address."""
        return self._reverse_lookup(ip_address)
