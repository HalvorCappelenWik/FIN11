import pandas as pd
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import hstack

nltk.download('stopwords')
nltk.download('words')
nltk.download('punkt')

# Set of English words and stopwords
english_words = set(words.words())
stop_words = set(stopwords.words('english'))

def preprocess_tweet(tweet):
    tokens = word_tokenize(tweet)
    cleaned_tokens = [token.lower() for token in tokens if token.lower() in english_words and 
                      token.lower() not in stop_words and token.isalpha()]
    return ' '.join(cleaned_tokens)

# Load dataset
dataset = pd.read_csv("last_dataset2.csv", delimiter=",")

# Preprocess tweets
dataset['Text'] = dataset['Text'].apply(preprocess_tweet)

# Split dataset into features and labels
tweetsAndSentiment = dataset[['Text', 'Sentiment']]
rank = dataset['Rank']

# Split tweetsAndSentiment into text and sentiment features
X_text = tweetsAndSentiment['Text']
X_sentiment = tweetsAndSentiment['Sentiment']
y = rank

# Split data
X_text_train, X_text_test, X_sentiment_train, X_sentiment_test, y_train, y_test = train_test_split(X_text, X_sentiment, y, test_size=0.30, random_state=42)

# Vectorize text data
vectorizer = CountVectorizer()
X_text_train_counts = vectorizer.fit_transform(X_text_train)
X_text_test_counts = vectorizer.transform(X_text_test)

# Scale sentiment to be non-negative
X_sentiment_train = (np.array(X_sentiment_train) + 1).reshape(-1, 1)  # scaling to [0, 2]
X_sentiment_test = (np.array(X_sentiment_test) + 1).reshape(-1, 1)    # scaling to [0, 2]

# Combine text features with scaled sentiment
X_train_combined = hstack([X_text_train_counts, X_sentiment_train])
X_test_combined = hstack([X_text_test_counts, X_sentiment_test])

# Train Multinomial Naive Bayes classifier
multinomial_clf = MultinomialNB()
multinomial_clf.fit(X_train_combined, y_train)

# Train Bernoulli Naive Bayes classifier
bernoulli_clf = BernoulliNB()
bernoulli_clf.fit(X_train_combined, y_train)

# Evaluate the Multinomial model
multinomial_pred = multinomial_clf.predict(X_test_combined)
multinomial_accuracy = accuracy_score(y_test, multinomial_pred)

# Evaluate the Bernoulli model
bernoulli_pred = bernoulli_clf.predict(X_test_combined)
bernoulli_accuracy = accuracy_score(y_test, bernoulli_pred)

# Print accuracy scores
print(f"Multinomial Naive Bayes Accuracy: {multinomial_accuracy}")
print(f"Bernoulli Naive Bayes Accuracy: {bernoulli_accuracy}")

# Function to plot confusion matrix as a table with colored columns
def plot_confusion_matrix_as_table(cm, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    col_labels = sorted(set(y_test))
    the_table = ax.table(cellText=cm, colLabels=col_labels, rowLabels=col_labels, 
                         cellLoc='center', loc='center')
    ax.text(0.5, 0.67, 'Predicted', ha='center', va='center', transform=ax.transAxes, fontsize=10, fontweight='bold')
    ax.text(-0.05, 0.5, 'Actual', ha='center', va='center', rotation='vertical', transform=ax.transAxes, fontsize=10, fontweight='bold')
    plt.title(title)
    plt.show()

# Compute confusion matrices
multinomial_conf_mat = confusion_matrix(y_test, multinomial_pred)
bernoulli_conf_mat = confusion_matrix(y_test, bernoulli_pred)

# Plot confusion matrices as tables
plot_confusion_matrix_as_table(multinomial_conf_mat, "Confusion Matrix - Multinomial Naive Bayes")
plot_confusion_matrix_as_table(bernoulli_conf_mat, "Confusion Matrix - Bernoulli Naive Bayes")
