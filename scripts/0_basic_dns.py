from dnsclient import DNSClient
from tabulate import tabulate


DOMAIN = "unizar.es"  # Universidad de Zaragoza

dns = DNSClient()

a_records = dns.get_a_record(DOMAIN)
ip_address = a_records[0] if a_records else None
dns_records = dns.get_ns_record(DOMAIN)
web_records = dns.get_web_record(DOMAIN)
mx_records = dns.get_mx_record(DOMAIN)
reverse_lookup = dns.reverse_lookup(ip_address)


def remove_trailing_dot(records):
    return [r[:-1] if r.endswith(".") else r for r in records]


table = [
    [
        DOMAIN,
        ip_address,
        ", ".join(remove_trailing_dot(dns_records)),
        ", ".join(remove_trailing_dot(web_records)),
        ", ".join(remove_trailing_dot(mx_records)),
    ]
]
headers = ["domain", "address", "adns", "web", "mail"]

with open("data/0_basic_dns.tex", "w", encoding="utf-8") as f:
    f.write(tabulate(table, headers=headers, tablefmt="latex"))
