import pandas as pd
import string

def remove_punctuation_and_url(s):
    if isinstance(s, str):  
        no_punctuation = s.translate(str.maketrans('', '', string.punctuation))
        return no_punctuation.replace("url", "")  
    return s

df = pd.read_csv('final_results.csv')

df['Text'] = df['Text'].apply(remove_punctuation_and_url)

df = df.drop(['Forventet_Avkastning', 'Faktisk_Avkastning', 'Unormal_Avkastning', 'Lopenummer'], axis=1)

df.to_csv('last_dataset.csv', index=False)

