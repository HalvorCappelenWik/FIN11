import pandas as pd
from sklearn.utils import shuffle

data = pd.read_csv("data/tweets/Tweets_Processed_10-23.csv")

data['Datetime'] = pd.to_datetime(data['Datetime'])

# Shuffle the dataset but keep the original index
shuffled_data = shuffle(data, random_state=42).reset_index(drop=True)

# Split
split_idx = int(len(shuffled_data) * 0.65)  # 65% of the dataset

train_data = shuffled_data.iloc[:split_idx]
test_data = shuffled_data.iloc[split_idx:]

train_data = train_data.sort_values('Datetime')
test_data = test_data.sort_values('Datetime')

train_data.to_csv("train_dataset.csv", index=False)
test_data.to_csv("test_dataset.csv", index=False)

