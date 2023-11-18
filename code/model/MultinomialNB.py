import pandas as pd
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('words')
nltk.download('punkt')

# Set of English words
english_words = set(words.words())

# Set of English stopwords
stop_words = set(stopwords.words('english'))

def preprocess_tweet(tweet):
    # Tokenize the tweet
    tokens = word_tokenize(tweet)

    # Remove words not in NLTK words list, stopwords, and punctuation
    cleaned_tokens = [token.lower() for token in tokens if token.lower() in english_words and 
                        token.lower() not in stop_words and token.isalpha()]

    # Return the cleaned tweet
    return ' '.join(cleaned_tokens)

# List of dataset filenames
datasets = ["tweets_0.001.csv", "tweets_0.002.csv", "tweets_0.003.csv", "tweets_0.004.csv", "tweets_0.005.csv"]

# Initialize a dictionary to store results
results = {}

for dataset in datasets:
    # Load data
    tweets = pd.read_csv(f"data/tweets/{dataset}", delimiter=",")

    # Preprocess tweets and split into texts and labels
    tweets['Text'] = tweets['Text'].apply(preprocess_tweet)
    texts = tweets['Text']
    labels = tweets['Rank']

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
    accuracy = accuracy_score(y_test, y_pred)

    # Store results
    results[dataset] = accuracy

    # Compute and plot the confusion matrix
    conf_mat = confusion_matrix(y_test, y_pred)
    conf_mat_df = pd.DataFrame(conf_mat, 
                               index=[f'Actual {label}' for label in sorted(set(y_test))], 
                               columns=[f'Predicted {label}' for label in sorted(set(y_test))])

    # Plot the confusion matrix as a table
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=conf_mat_df.values, 
                         colLabels=conf_mat_df.columns, 
                         rowLabels=conf_mat_df.index, 
                         loc='center',
                         cellLoc='center')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    plt.title(f'Confusion Matrix for {dataset}')
    plt.show()

# Plotting the results for comparison
datasets = list(results.keys())
accuracies = list(results.values())

plt.figure(figsize=(10, 5))
plt.bar(datasets, accuracies, color='skyblue')
plt.xlabel('Datasets')
plt.ylabel('Accuracy')
plt.title('Comparison of Model Accuracies Across Different Datasets')
plt.xticks(rotation=45)
plt.show()
