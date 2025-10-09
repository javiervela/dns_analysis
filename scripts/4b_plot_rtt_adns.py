import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ADNS_RTT_FILE = "data/adns_rtt.csv"
# ADNS_RTT_FILE_1 = "data/adns_rtt_1.csv"
# ADNS_RTT_FILE_2 = "data/adns_rtt_2.csv"
LDNS_INPUT_FILE = "data/ldns.csv"
HOSTNAMES_INPUT_FILE = "data/hostnames.csv"

adns_measurements_df = pd.concat(
    [
        pd.read_csv(f)
        for f in [
            ADNS_RTT_FILE,
            # ADNS_RTT_FILE_1,
            # ADNS_RTT_FILE_2,
        ]
    ],
    ignore_index=True,
)

adns_measurements_df["LDNS_ADNS_RTT"] = (
    adns_measurements_df["ADNS_RTT"] - adns_measurements_df["LDNS_RTT"]
)

adns_rtt_df = (
    adns_measurements_df.groupby(["LDNS", "Hostname"])
    .agg(
        {
            "ADNS_RTT": "median",
            "LDNS_RTT": "median",
            "LDNS_ADNS_RTT": "median",
        }
    )
    .reset_index()
)

# adns_rtt_df["LDNS_ADNS_RTT"] = adns_rtt_df["ADNS_RTT"] - adns_rtt_df["LDNS_RTT"]


heatmap_data = adns_rtt_df.pivot(
    index="LDNS", columns="Hostname", values="LDNS_ADNS_RTT"
)

plt.figure(figsize=(8, 6))
sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    center=0,
    cmap="bwr",
    cbar_kws={"label": "LDNS_ADNS_RTT"},
)
plt.ylabel("LDNS")
plt.xlabel("Hostname")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("data/ldns_adns_rtt_heatmap.png")

total_ldns_rtt = adns_rtt_df.groupby("LDNS")["LDNS_ADNS_RTT"].sum().reset_index()

total_adns_rtt = adns_rtt_df.groupby("Hostname")["LDNS_ADNS_RTT"].sum().reset_index()

print(total_ldns_rtt)

print(total_adns_rtt)
