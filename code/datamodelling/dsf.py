import pandas as pd

# Load the DataFrame
df = pd.read_csv("data/tweets/tweets_0.001.csv")

# Strip the Text column 
df['Text'] = df['Text'].str.replace(r'[^\w\s]', '', regex=True)  # This will also remove commas

df.to_csv("trading_test.csv", index=False)
