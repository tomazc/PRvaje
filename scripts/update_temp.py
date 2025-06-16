import pandas as pd

url = "https://bolin.su.se/data/data/stockholm_daily_mean_temperature.csv"
data = pd.read_csv(url)
df = data['date'].str.split("-", expand=True).rename(columns={0: "Year", 1: "Month", 2: "Day"})
df["Temp"] = data["raw"]
df = df[df["Temp"] != -999]
df.to_csv('notebooks/data/stockholm.csv', index=False)  