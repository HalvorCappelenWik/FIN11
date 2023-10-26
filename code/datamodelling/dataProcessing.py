import pandas as pd
import re
import pytz

df = pd.read_csv('data/tweets/tweets_10-23.csv', encoding='latin1')

df = df[["Datetime", "Text"]]

df = df[::-1].reset_index(drop=True)

# Replace URLs in 'Text' with "{URL}"
for i in range(len(df)):
    if "http" in df["Text"][i]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', df["Text"][i])
        for url in urls:
            df["Text"][i] = df["Text"][i].replace(url, '{URL}')

# Convert 'Datetime' column to datetime objects and set as UTC
df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True)

# Set 'Datetime' as the index
df = df.set_index('Datetime')

# Convert 'Datetime' index from UTC to EDT
est_zone = pytz.timezone('America/New_York')
df.index = df.index.tz_convert(est_zone)

# Save to CSV
df.to_csv('data/Tweets_Processed_10-23_EST.csv')

# Make text lowercase
df["Text"] = df["Text"].str.lower()

# Filter for tweets containing "tesla" or "tsla"
tesla_df = df[df["Text"].str.contains("tesla|tsla")]

# Save to CSV
tesla_df.to_csv('data/Tweets_Only_TSLA_EST.csv')
