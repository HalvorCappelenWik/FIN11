from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pandas as pd

# Sample data
tweets = pd.read_csv("data/tweets/dataMedRank2.csv", delimiter=";")

# Split tweets and labels
texts = tweets["Text"]
labels = tweets["Rank"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.30, random_state=42)

# Convert text to a matrix of token counts
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)

# Train Naive Bayes classifier
clf = MultinomialNB()
clf.fit(X_train_counts, y_train)

# Evaluate the model
X_test_counts = vectorizer.transform(X_test)
y_pred = clf.predict(X_test_counts)
print("Accuracy:", accuracy_score(y_test, y_pred))

