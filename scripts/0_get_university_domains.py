import pandas as pd

INPUT_FILE = "data/Colleges.csv"
OUTPUT_FILE = "data/universities.csv"

df = pd.read_csv(INPUT_FILE)
universities = df[["Institution's internet website address (HD2020)"]]
universities.columns = ["Domain"]
universities = universities.dropna()
universities = universities.sample(100, random_state=42).reset_index(drop=True)
universities["Domain"] = universities["Domain"].str.replace(
    r"https?://", "", regex=True
)
universities["Domain"] = universities["Domain"].str.replace(r"^www\.", "", regex=True)
universities["Domain"] = universities["Domain"].str.replace(r"/.*$", "", regex=True)
universities = universities.sort_values(by="Domain").reset_index(drop=True)
universities.to_csv(OUTPUT_FILE, index=False)
