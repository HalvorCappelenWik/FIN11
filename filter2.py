import pandas as pd
import string
from textblob import TextBlob

def remove_punctuation_and_url(s):
    if isinstance(s, str):  
        no_punctuation = s.translate(str.maketrans('', '', string.punctuation))
        return no_punctuation.replace("url", "")  
    return s

df = pd.read_csv('final_results_sec.csv')

df['Text'] = df['Text'].apply(remove_punctuation_and_url)

# Remove all colums except for the last 3 
df = df.iloc[:, -3:]

# Make datetime column first, then text, then rank
df = df[['Datetime', 'Text', 'Rank']]

# Save the updated DataFrame

df.to_csv('final_results_sec.csv', index=False)


#make a copy of last_dataset2.csv but remove the column "Sentiment"
df2 = pd.read_csv('last_dataset2.csv')
df2 = df2.drop(columns=['Sentiment'])
df2.to_csv('last_dataset3.csv', index=False)
