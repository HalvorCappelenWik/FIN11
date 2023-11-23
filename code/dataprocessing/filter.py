import pandas as pd
import string
from textblob import TextBlob

def remove_punctuation_and_url(s):
    if isinstance(s, str):  
        no_punctuation = s.translate(str.maketrans('', '', string.punctuation))
        return no_punctuation.replace("url", "")  
    return s

def get_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)
    # Return the polarity
    return blob.sentiment.polarity

# Load your DataFrame
df = pd.read_csv('data/tweets/last_dataset.csv')

# Clean the text
df['Text'] = df['Text'].apply(remove_punctuation_and_url)


# Apply sentiment analysis
df['Sentiment'] = df['Text'].apply(get_sentiment)

# Save the updated DataFrame
df.to_csv('last_dataset2.csv', index=False)
