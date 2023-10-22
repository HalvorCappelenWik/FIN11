import pandas as pd
import re

df = pd.read_csv('data/Tweets_10-23.csv', encoding='latin1')

df = df[["Datetime", "Text"]]

df = df[::-1].reset_index(drop = True)

for i in range(0, len(df)):
    if "http" in df["Text"][i]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', df["Text"][i])

        #Replace all urls with {URL}
        for url in urls:
            df["Text"][i] = df["Text"][i].replace(url, '{URL}')

#Lagrer til ny csv
df.to_csv('data/Tweets_Processed_10-23.csv', index = False)

# Make all tweets lowercase and create a csv with all tweets that has "tesla" or "tsla" in it
df["Text"] = df["Text"].str.lower()
df = df[df["Text"].str.contains("tesla|tsla")]

df.to_csv('data/Tweets_Processed_10-23_TSLA.csv', index = False)


print(df.head())