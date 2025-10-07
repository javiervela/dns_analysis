from time import time, sleep
import pandas as pd
from dnsclient import DNSClient

LDNS_INPUT_FILE = "data/ldns.csv"
HOSTNAMES_INPUT_FILE = "data/hostnames.csv"

ldns_df = pd.read_csv(LDNS_INPUT_FILE)
hostnames_df = pd.read_csv(HOSTNAMES_INPUT_FILE)

ldns = ldns_df["IP"].tolist()
hostnames = hostnames_df["Hostname"].tolist()

client = DNSClient()
data = []

while True:
    try:
        for l in ldns:
            for u in hostnames:
                response = client.get_a_record(domain=u, dns_server=l, norecurse=True)
                hit = True if response else False
                hit_time = time()
                data.append((l, u, hit, hit_time))
                print(f"Response for {l} and {u}: {hit}")
        sleep(300)
    except KeyboardInterrupt:
        break

df = pd.DataFrame(data, columns=["LDNS", "Hostname", "Hit", "Timestamp"])
df.to_csv(f"data/ldns_hits_{int(time())}.csv", index=False)
