import pandas as pd
from dnsclient import DNSClient

LDNS_INPUT_FILE = "data/ldns.csv"
HOSTNAMES_INPUT_FILE = "data/hostnames.csv"
OUTPUT_FILE = "data/adns_rtt.csv"

ldns_df = pd.read_csv(LDNS_INPUT_FILE)
hostnames_df = pd.read_csv(HOSTNAMES_INPUT_FILE)

ldns = ldns_df["IP"].tolist()
hostnames = hostnames_df["Hostname"].tolist()

client = DNSClient()

n_measurements = 10
test_domain_fmt = "hopefullythisdoesnotexist.{}"

data = [] 
for l in ldns:
    for h in hostnames:
        for _ in range(n_measurements):
            test_domain = test_domain_fmt.format(h)
            rtt = client.get_query_time(domain=test_domain, dns_server=l)
            data.append({"LDNS": l, "Hostname": h, "RTT": rtt})
            print(f"LDNS: {l}, Hostname: {h}, RTT: {rtt} ms")

df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)
