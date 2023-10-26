import pandas as pd
import re
import pytz

df = pd.read_csv('data/tweets/tweets_10-23.csv', encoding='latin1')

df = df[["Datetime", "Text"]]
df = df[::-1].reset_index(drop=True)

df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True)
df = df.set_index('Datetime')

# Convert 'Datetime' index from UTC to EST
est_zone = pytz.timezone('America/New_York')
df.index = df.index.tz_convert(est_zone)

# Filter rows between 09:30 and 16:00 EST
filtered_df = df.between_time('09:30', '16:00')
print("Total Number of rows between 09:30 and 16:00 EST:", len(filtered_df))

df["Text"] = df["Text"].str.lower()
df = df[df["Text"].str.contains("tesla|tsla")]

filtered_df = df.between_time('09:30', '16:00')
print("TSLA/Tesla Tweets between 09:30 and 16:00 EST:", len(filtered_df))
