"""Create a deliberately messy copy of the airline passengers dataset.

The original data is clean, so we inject realistic problems (missing values,
outliers, duplicates, missing timestamps) to practise cleaning on.
Run: python src/make_dirty_data.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
df = pd.read_csv("data/raw/airline-passengers.csv")
df.columns = ["Month", "Passengers"]
df["Passengers"] = df["Passengers"].astype(float)

df.loc[rng.choice(len(df), 8, replace=False), "Passengers"] = np.nan   # missing values
for i, factor in zip(rng.choice(len(df), 3, replace=False), [3.0, 0.2, 2.5]):
    df.loc[i, "Passengers"] *= factor                                  # outliers
df = df.drop(rng.choice(len(df), 2, replace=False))                    # missing timestamps
df = pd.concat([df, df.sample(2, random_state=1)])                     # duplicate rows
df = df.sample(frac=1, random_state=7)                                 # shuffle order
df.to_csv("data/raw/airline_passengers_dirty.csv", index=False)
print("Saved data/raw/airline_passengers_dirty.csv", df.shape)
