import pandas as pd
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

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

dataset = pd.read_csv("data/tweets/final_dataset.csv", delimiter=",")

# Preprocess tweets and split into texts and labels
dataset['Text'] = dataset['Text'].apply(preprocess_tweet)
tweets = dataset['Text']
rank = dataset['Rank']

# Split data
X_train, X_test, y_train, y_test = train_test_split(tweets, rank, test_size=0.30, random_state=42)

# Convert text to a matrix of token counts
vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)

# Train Multinomial Naive Bayes classifier
multinomial_clf = MultinomialNB()
multinomial_clf.fit(X_train_counts, y_train)

# Train Bernoulli Naive Bayes classifier
bernoulli_clf = BernoulliNB()
bernoulli_clf.fit(X_train_counts, y_train)

# Evaluate the Multinomial model
X_test_counts = vectorizer.transform(X_test)
multinomial_pred = multinomial_clf.predict(X_test_counts)
multinomial_accuracy = accuracy_score(y_test, multinomial_pred)

# Evaluate the Bernoulli model
bernoulli_pred = bernoulli_clf.predict(X_test_counts)
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
    cell_colors = [["w" if col_label not in [-1, 0, 1] else '#FFDDC1' if col_label == -1 
                    else '#C1FFD7' if col_label == 0 else '#C1D7FF' for col_label in col_labels] 
                    for _ in range(len(cm))]

    # Create a table with confusion matrix data and colored cells for specific columns
    the_table = ax.table(cellText=cm, colLabels=col_labels, rowLabels=col_labels, 
                         cellLoc='center', loc='center', cellColours=cell_colors)

    # Adding labels for clarity
    ax.text(0.5, 0.70, 'Predicted', ha='center', va='center', transform=ax.transAxes, fontsize=10, fontweight='bold')
    ax.text(-0.1, 0.5, 'Actual', ha='center', va='center', rotation='vertical', transform=ax.transAxes, fontsize=10, fontweight='bold')

    plt.title(title)
    plt.show()

# Compute confusion matrices
multinomial_conf_mat = confusion_matrix(y_test, multinomial_pred)
bernoulli_conf_mat = confusion_matrix(y_test, bernoulli_pred)

# Plot confusion matrices as tables
plot_confusion_matrix_as_table(multinomial_conf_mat, "Confusion Matrix - Multinomial Naive Bayes")
plot_confusion_matrix_as_table(bernoulli_conf_mat, "Confusion Matrix - Bernoulli Naive Bayes")


