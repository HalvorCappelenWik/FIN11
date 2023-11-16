import pandas as pd
import re
import pytz
import pandas as pd
from sklearn.utils import shuffle

df = pd.read_csv('data/tweets/tweets.csv', encoding='latin1')
df = df[["Datetime", "Text"]]
df = df[::-1].reset_index(drop=True)

for i in range(len(df)):
    if "http" in df["Text"][i]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', df["Text"][i])
        for url in urls:
            df["Text"][i] = df["Text"][i].replace(url, '{URL}')

# Convert 'Datetime' column to datetime objects and set as UTC
df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True)

# Set 'Datetime' as the index
df = df.set_index('Datetime')

# Convert 'Datetime' index from UTC to EST 
est_zone = pytz.timezone('America/New_York')
df.index = df.index.tz_convert(est_zone)

df_all = df.copy()
df_tsla = df.copy()

# Save to CSV
df_all.to_csv('data/tweets/df_all_tweets.csv')

# Make text lowercase
df_tsla["Text"] = df_tsla["Text"].str.lower()
df_tsla = df_tsla[df_tsla["Text"].str.contains("tesla|tsla|elon|musk|elonmusk|model3|model 3|modely|model y|modelx|model x|model s|models3|models|cybertr")]

df_tsla.to_csv('data/tweets/df_tsla.csv')

df_opening_hours = df_tsla.between_time('09:30', '16:00')

df_opening_hours.index = pd.to_datetime(df_opening_hours.index)
df_opening_hours.index = df_opening_hours.index.strftime('%Y-%m-%d %H:%M:%S')

df_opening_hours.to_csv('data/tweets/df_tsla_opening_hours.csv')

TrainTestData = pd.read_csv("data/tweets/df_tsla_opening_hours.csv")

TrainTestData['Datetime'] = pd.to_datetime(TrainTestData['Datetime'])

# Shuffle the dataset but keep the original index
shuffled_data = shuffle(TrainTestData, random_state=42).reset_index(drop=True)

# Split
split_idx = int(len(shuffled_data) * 0.70)  # 70% of the dataset

train_data = shuffled_data.iloc[:split_idx]
test_data = shuffled_data.iloc[split_idx:]

train_data = train_data.sort_values('Datetime')
test_data = test_data.sort_values('Datetime')

train_data.to_csv("data/tweets/train_dataset.csv", index=False)
test_data.to_csv("data/tweets/test_dataset.csv", index=False)


