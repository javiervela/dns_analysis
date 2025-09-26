import pandas as pd
from dnsclient import DNSClient
from tqdm import tqdm


INPUT_FILE = "data/universities.csv"
OUTPUT_FILE = "data/universities_nameservers.csv"


df = pd.read_csv(INPUT_FILE)

dns = DNSClient()

results = []

for domain in tqdm(df["Domain"], desc="Processing domains"):
    dns_records = dns.get_ns_record(domain)
    web_records = dns.get_web_record(domain)
    mx_records = dns.get_mx_record(domain)

    results.append(
        {"Domain": domain, "ADNS": dns_records, "Web": web_records, "Mail": mx_records}
    )

df = pd.DataFrame(results)


def remove_trailing_dot(records):
    return [r[:-1] if r.endswith(".") else r for r in records]


df["ADNS"] = df["ADNS"].apply(lambda x: remove_trailing_dot(x))
df["Web"] = df["Web"].apply(lambda x: remove_trailing_dot(x))
df["Mail"] = df["Mail"].apply(lambda x: remove_trailing_dot(x))

df.to_csv(OUTPUT_FILE, index=False)
