from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pandas as pd

# Sample data
tweets = pd.read_csv("data/tweets/DataMedRank2.csv", delimiter=";")

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

# Print the first 10 predictions
print("Predictions:", clf.predict(X_test_counts[:100]))

# Print the first 10 actual labels
print("Actual:", y_test[:100].values)

# Store all the actual labels and predictions in a dataframe and the tweet text 
df_pred = pd.DataFrame({"Actual": y_test, "Predicted": y_pred, "Text": X_test})
df_pred.to_csv("data/tweets/df_pred.csv", index=False)
