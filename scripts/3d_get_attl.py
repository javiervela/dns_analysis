import pandas as pd

from dnsclient import DNSClient

HOSTNAMES_INPUT_FILE = "data/hostnames.csv"

hostnames_df = pd.read_csv(HOSTNAMES_INPUT_FILE)

client = DNSClient()

attl_data = []
for _, row in hostnames_df.iterrows():
    hostname = row["Hostname"]
    attl = client.get_attl(hostname)
    print(f"Hostname: {hostname}, ATTL: {attl}")
    attl_data.append(attl)

hostnames_df["ATTL"] = attl_data

hostnames_df.to_csv("data/hostnames_attl.csv", index=False)
# to latex table save
with open("data/hostnames_attl.tex", "w") as f:
    f.write(hostnames_df[["Hostname", "ATTL"]].to_latex(index=False))
