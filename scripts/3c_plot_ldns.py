import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# INPUT_FILE = "data/ldns_hits_1.csv"
INPUT_FILE = "data/ldns_hits_2.csv"

LDNS_INPUT_FILE = "data/ldns.csv"
HOSTNAMES_INPUT_FILE = "data/hostnames.csv"

ldns_df = pd.read_csv(LDNS_INPUT_FILE)
hostnames_df = pd.read_csv(HOSTNAMES_INPUT_FILE)

ldns = ldns_df["IP"].tolist()
hostnames = hostnames_df["Hostname"].tolist()

dns_data_df = pd.read_csv(INPUT_FILE)
grouped = dns_data_df.groupby(["LDNS", "Hostname"])
heatmap_data = grouped["Hit"].sum().unstack(fill_value=0)

heatmap_data = heatmap_data.reindex(index=ldns, columns=hostnames, fill_value=0)

row_sums = heatmap_data.sum(axis=1)
heatmap_percent = heatmap_data.div(row_sums, axis=0).fillna(0)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_percent, annot=True, fmt=".2f", cmap="YlGnBu")
plt.title("LDNS Hits Heatmap (Percentages)")
plt.xlabel("Hostname")
plt.ylabel("LDNS")
plt.tight_layout()
plt.savefig("data/ldns_hits_heatmap.png")

# print the min and max "time" in day time
dns_data_df["Timestamp"] = pd.to_datetime(dns_data_df["Timestamp"], unit='s')
print("Min Timestamp:", dns_data_df["Timestamp"].min())
print("Max Timestamp:", dns_data_df["Timestamp"].max())
