import pandas as pd 
import re
import pytz
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
import string

if not nltk.data.find('corpora/stopwords'):
    nltk.download('stopwords')
if not nltk.data.find('corpora/words'):
    nltk.download('words')
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt')


# English words and stopwords
english_words = set(words.words())
stop_words = set(stopwords.words('english'))

# Function to remove punctuation and URLs from a string
def remove_punctuation_and_url(s):
    no_punctuation = s.translate(str.maketrans('', '', string.punctuation))
    return re.sub(r'http\S+', '', no_punctuation)

# Function to tokenize, remove stopwords, non-English words, and convert to lowercase
def tokenize_and_clean(tweet):
    tokens = word_tokenize(tweet)
    cleaned_tokens = [token.lower() for token in tokens if token.lower() in english_words 
                      and token.lower() not in stop_words and token.isalpha()]
    return ' '.join(cleaned_tokens)

# Function to get the sentiment of a tweet 
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Function to preprocess tweets
def preprocess_tweets(df):
    df['Cleaned_Text'] = df['Text'].apply(lambda x: tokenize_and_clean(remove_punctuation_and_url(x)))
    df['Sentiment'] = df['Cleaned_Text'].apply(get_sentiment)
    return df

# Process Data
df = pd.read_csv('data/tweets/tweets.csv', encoding='latin1')
df = df[["Datetime", "Text"]][::-1].reset_index(drop=True)
df['Datetime'] = pd.to_datetime(df['Datetime'], utc=True).dt.tz_convert(pytz.timezone('America/New_York'))
df.set_index('Datetime', inplace=True)
df = df[df["Text"].str.contains("tesla|tsla|elon|musk|elonmusk|model3|model 3|modely|model y|modelx|model x|" +
                                "model s|models3|models|cybertr")]
df = df.between_time('09:30', '16:00')
df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
df_tsla = preprocess_tweets(df)

# Output data 
df_tsla.to_csv('data/tweets/df_tsla.csv')



