import pandas as pd
from collections import Counter


INPUT_FILE = "data/universities_nameservers.csv"

DOMAIN_TEX_FILE = "data/2_universities_nameservers.tex"


df = pd.read_csv(INPUT_FILE)

df["ADNS"] = df["ADNS"].apply(eval)
df["Web"] = df["Web"].apply(eval)
df["Mail"] = df["Mail"].apply(eval)

df["ADNS"] = df["ADNS"].apply(lambda x: [i for i in x if i])
df["Web"] = df["Web"].apply(lambda x: [i for i in x if i])
df["Mail"] = df["Mail"].apply(lambda x: [i for i in x if i])

df["ADNS_len"] = df["ADNS"].apply(len)
df["Web_len"] = df["Web"].apply(len)
df["Mail_len"] = df["Mail"].apply(len)

df_filered = df[(df["ADNS_len"] > 0) & (df["Web_len"] > 0) & (df["Mail_len"] > 0)]


def extract_server_domain(service_list, domain):
    server_domains = []
    for s in service_list:
        parts = s.split(".")
        if len(parts) >= 2:
            server_domains.append(parts[-2] + "." + parts[-1])
        else:
            server_domains.append(s)
            
    if domain in server_domains:
        return [domain]
    elif server_domains:
        return [server_domains[0]]
    else:
        return []


for service in ["ADNS", "Web", "Mail"]:
    df_filered[service] = df_filered.apply(
        lambda row: extract_server_domain(row[service], row["Domain"]), axis=1
    )


def format_latex(s):
    return s.replace("_", "\\_")


df_filered["Domain"] = df_filered["Domain"].apply(format_latex)
df_filered["ADNS"] = df_filered["ADNS"].apply(lambda x: [format_latex(i) for i in x])
df_filered["Web"] = df_filered["Web"].apply(lambda x: [format_latex(i) for i in x])
df_filered["Mail"] = df_filered["Mail"].apply(lambda x: [format_latex(i) for i in x])


latex_table = df_filered[
    ["Domain", "ADNS", "ADNS_len", "Web", "Web_len", "Mail", "Mail_len"]
]

with open(DOMAIN_TEX_FILE, "w", encoding="utf-8") as f:
    f.write("\\begin{tabular}{l l r l r l r}\n")
    f.write("\\hline\n")
    f.write("Domain & ADNS & Cnt & Web & Cnt & Mail & Cnt \\\\\n")
    f.write("\\hline\n")
    for _, row in latex_table.iterrows():
        adns = ", ".join(row["ADNS"])
        web = ", ".join(row["Web"])
        mail = ", ".join(row["Mail"])
        f.write(
            f"{row['Domain']} & {adns} & {row['ADNS_len']} & {web} & {row['Web_len']} & {mail} & {row['Mail_len']} \\\\\n"
        )
    f.write("\\hline\n")
    f.write("\\end{tabular}\n")


total_domains = len(df_filered)

own_service_counts = {}
for service in ["ADNS", "Web", "Mail"]:
    own_service_counts[service] = df_filered.apply(
        lambda row: row["Domain"] in row[service], axis=1
    ).sum()

for service in ["ADNS", "Web", "Mail"]:
    percentage = (own_service_counts[service] / total_domains) * 100
    print(f"Percentage of domains providing their own {service}: {percentage:.2f}%")


def simplify_provider_name(name):
    name_lower = name.lower()
    if "aws" in name_lower or "amazonaws" in name_lower:
        return "aws.amazon.com"
    elif "azure" in name_lower:
        return "azure.microsoft.com"
    elif "google" in name_lower:
        return "google.com"
    else:
        return name


df_providers = df_filered.copy()

for service in ["ADNS", "Web", "Mail"]:
    df_providers[service] = df_providers[service].apply(
        lambda providers: [simplify_provider_name(p) for p in providers]
    )

    all_providers = [
        provider for providers in df_providers[service] for provider in providers
    ]
    top5 = Counter(all_providers).most_common(5)
    print(f"Top 5 {service} providers:")
    for provider, count in top5:
        print(f"  {provider}: {count}")


for service in ["ADNS", "Web", "Mail"]:
    print(f"Statistics for {service} server counts:")
    counts_series = df_filered[service + "_len"]
    print(f"  Mean: {counts_series.mean():.2f}")
    print(f"  Min: {counts_series.min()}")
    print(f"  Max: {counts_series.max()}")
    print(f"  Median: {counts_series.median()}")
