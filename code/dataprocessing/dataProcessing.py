import pandas as pd
import re
import pytz
import pandas as pd

df = pd.read_csv('data/tweets/tweets.csv', encoding='latin1')
df = df[["Datetime", "Text"]]
df = df[::-1].reset_index(drop=True)

for i in range(len(df)):
    if "http" in df["Text"][i]:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', df["Text"][i])
        for url in urls:
            df["Text"][i] = df["Text"][i].replace(url, '')

df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True)

df = df.set_index('Datetime')

est_zone = pytz.timezone('America/New_York')
df.index = df.index.tz_convert(est_zone)

df_all = df.copy()
df_tsla = df.copy()

df_tsla["Text"] = df_tsla["Text"].str.lower()
df_tsla = df_tsla[df_tsla["Text"].str.contains("tesla|tsla|elon|musk|elonmusk|model3|model 3|modely|model y|modelx|model x|model s|models3|models|cybertr")]

df_tsla.to_csv('data/tweets/df_tsla.csv')

df_opening_hours = df_tsla.between_time('09:30', '16:00')

df_opening_hours.index = pd.to_datetime(df_opening_hours.index)
df_opening_hours.index = df_opening_hours.index.strftime('%Y-%m-%d %H:%M:%S')

df_opening_hours.to_csv('data/tweets/df_tsla_opening_hours.csv')


