import pandas as pd
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Define the text preprocessing function
def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Lowercase
    tokens = [word.lower() for word in tokens]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join tokens back into a single string
    return ' '.join(tokens)

# Sample data
tweets = pd.read_csv("data/tweets/tweets_0.005.csv", delimiter=",", encoding='latin1')

# Preprocess the text data
tweets['Text'] = tweets['Text'].apply(preprocess_text)

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


# Compute and plot the confusion matrix
conf_mat = confusion_matrix(y_test, y_pred)
conf_mat_df = pd.DataFrame(conf_mat, 
                            index=[f'Actual {label}' for label in sorted(set(y_test))], 
                            columns=[f'Predicted {label}' for label in sorted(set(y_test))])

# Plot the confusion matrix as a table
fig, ax = plt.subplots(figsize=(8, 4))  # Adjust to fit your data
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=conf_mat_df.values, 
                        colLabels=conf_mat_df.columns, 
                        rowLabels=conf_mat_df.index, 
                        loc='center',
                        cellLoc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)
plt.show()

