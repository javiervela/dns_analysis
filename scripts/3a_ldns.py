import pandas as pd

from dnsclient import DNSClient

INPUT_FILE = "data/ldns.csv"
OUTPUT_FILE = "data/ldns.csv"

df = pd.read_csv(INPUT_FILE)

client = DNSClient()


def remove_trailing_dot(records):
    return [r[:-1] if r.endswith(".") else r for r in records]


test_hostname = "wpi.edu"

df["Hostname"] = df["IP"].apply(
    lambda ip: (remove_trailing_dot(client.reverse_lookup(ip)) or [None])[0]
)
df["Works"] = df["IP"].apply(lambda ip: client.get_a_record(test_hostname, ip) != [])

df.to_csv(OUTPUT_FILE, index=False)
