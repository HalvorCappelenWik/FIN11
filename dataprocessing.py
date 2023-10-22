import pandas as pd
import re 

df = pd.read_csv('data/Tweets_12-17.csv', encoding='latin1')

df = df[["Time", "Tweet"]]

#Reverserer rekkefølge
df = df[::-1].reset_index(drop = True)


for i in range(0, len(df)):
    if "http" in df["Tweet"][i]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', df["Tweet"][i])

        for url in urls:
            df["Tweet"][i] = df["Tweet"][i].replace(url, '{URL}')


#Lagrer til ny csv
df.to_csv('data/Tweets_Processed2.csv', index = False)


print(df.head())
print(df.info())

