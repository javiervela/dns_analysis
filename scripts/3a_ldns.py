import pandas as pd
from time import sleep

from dnsclient import DNSClient

INPUT_FILE = "data/ldns.csv"
TEX_FILE = "data/3_ldns_rtt.tex"

df = pd.read_csv(INPUT_FILE)

client = DNSClient()


def remove_trailing_dot(records):
    return [r[:-1] if r.endswith(".") else r for r in records]


test_hostname = "google.com"

df["Hostname"] = df["IP"].apply(
    lambda ip: (remove_trailing_dot(client.reverse_lookup(ip_address=ip)) or [None])[0]
)

df["A Record"] = df["IP"].apply(
    lambda ip: (
        client.get_a_record(domain=test_hostname, dns_server=ip, norecurse=True)
        or [None]
    )[0]
)
df["Works"] = df["A Record"].apply(lambda record: record is not None and record != "")
df["RTT"] = df["IP"].apply(
    lambda ip: client.get_query_time(
        domain=test_hostname, dns_server=ip, norecurse=True
    )
)

df.to_csv(INPUT_FILE, index=False)

df = df.sort_values(by="RTT")
df.to_latex(
    TEX_FILE,
    index=False,
    columns=["IP", "Hostname", "RTT"],
    header=["LDNS IP", "Hostname", "RTT (ms)"],
    na_rep="N/A",
    longtable=True,
    caption="LDNS Response Times",
    label="tab:ldns_rtt",
)
