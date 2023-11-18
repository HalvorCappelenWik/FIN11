import pandas as pd
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
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
datasets = ["final_dataset.csv"]

# Initialize dictionaries to store results
results_multinomial = {}
results_bernoulli = {}

for dataset in datasets:
    # Load data
    tweets = pd.read_csv(f"data/tweets/{dataset}", delimiter=";")

    # Preprocess tweets and split into texts and labels
    tweets['Text'] = tweets['Text'].apply(preprocess_tweet)
    texts = tweets['Text']
    labels = tweets['Rank']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.30, random_state=42)

    # Vectorization for MultinomialNB
    vectorizer_multinomial = CountVectorizer()
    X_train_counts_multinomial = vectorizer_multinomial.fit_transform(X_train)
    X_test_counts_multinomial = vectorizer_multinomial.transform(X_test)

    # Vectorization for BernoulliNB
    vectorizer_bernoulli = CountVectorizer(binary=True)
    X_train_counts_bernoulli = vectorizer_bernoulli.fit_transform(X_train)
    X_test_counts_bernoulli = vectorizer_bernoulli.transform(X_test)

    # Train and evaluate Multinomial Naive Bayes classifier
    clf_multinomial = MultinomialNB()
    clf_multinomial.fit(X_train_counts_multinomial, y_train)
    y_pred_multinomial = clf_multinomial.predict(X_test_counts_multinomial)
    accuracy_multinomial = accuracy_score(y_test, y_pred_multinomial)
    results_multinomial[dataset] = accuracy_multinomial
    conf_mat_multinomial = confusion_matrix(y_test, y_pred_multinomial)

    # Train and evaluate Bernoulli Naive Bayes classifier
    clf_bernoulli = BernoulliNB()
    clf_bernoulli.fit(X_train_counts_bernoulli, y_train)
    y_pred_bernoulli = clf_bernoulli.predict(X_test_counts_bernoulli)
    accuracy_bernoulli = accuracy_score(y_test, y_pred_bernoulli)
    results_bernoulli[dataset] = accuracy_bernoulli
    conf_mat_bernoulli = confusion_matrix(y_test, y_pred_bernoulli)

    # Plot the confusion matrices for both classifiers
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Confusion Matrix for Multinomial Naive Bayes
    axes[0].axis('tight')
    axes[0].axis('off')
    table_multinomial = axes[0].table(cellText=conf_mat_multinomial, 
                                      rowLabels=[f'Actual {label}' for label in sorted(set(y_test))], 
                                      colLabels=[f'Predicted {label}' for label in sorted(set(y_test))],
                                      cellLoc='center', loc='center')
    table_multinomial.auto_set_font_size(False)
    table_multinomial.set_fontsize(10)
    axes[0].set_title(f'MultinomialNB Confusion Matrix\n{dataset}')
    
    # Confusion Matrix for Bernoulli Naive Bayes
    axes[1].axis('tight')
    axes[1].axis('off')
    table_bernoulli = axes[1].table(cellText=conf_mat_bernoulli, 
                                    rowLabels=[f'Actual {label}' for label in sorted(set(y_test))], 
                                    colLabels=[f'Predicted {label}' for label in sorted(set(y_test))],
                                    cellLoc='center', loc='center')
    table_bernoulli.auto_set_font_size(False)
    table_bernoulli.set_fontsize(10)
    axes[1].set_title(f'BernoulliNB Confusion Matrix\n{dataset}')

    plt.tight_layout()
    plt.show()

# Plotting the results for comparison
plt.figure(figsize=(12, 6))
bar_width = 0.35
index = range(len(datasets))

plt.bar(index, results_multinomial.values(), bar_width, label='MultinomialNB', color='b')
plt.bar([i + bar_width for i in index], results_bernoulli.values(), bar_width, label='BernoulliNB', color='r')

plt.xlabel('Datasets')
plt.ylabel('Accuracy')
plt.title('Comparison of Model Accuracies Across Different Datasets')
plt.xticks([i + bar_width / 2 for i in index], datasets, rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
