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
            rtt_adns = client.get_query_time(domain=test_domain, dns_server=l)
            rtt_ldns = client.get_query_time(
                domain=test_domain, dns_server=l, norecurse=True
            )
            data.append(
                {"LDNS": l, "Hostname": h, "ADNS_RTT": rtt_adns, "LDNS_RTT": rtt_ldns}
            )
            print(f"Measured {l} {h} {rtt_adns} {rtt_ldns}")

df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)
