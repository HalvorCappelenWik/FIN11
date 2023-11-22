import pandas as pd
import string

# Function to remove punctuation and occurrences of "url"
def remove_punctuation_and_url(s):
    if isinstance(s, str):  # Ensure the input is a string
        no_punctuation = s.translate(str.maketrans('', '', string.punctuation))
        return no_punctuation.replace("url", "")  # Remove "url"
    return s

df = pd.read_csv('final_dataset2.csv')

# Apply the function to the specific column
# Replace 'Text' with the name of your target column if it's different
df['Text'] = df['Text'].apply(remove_punctuation_and_url)

# Save the modified DataFrame
df.to_csv('final_dataset2.csv', index=False)

#count number of rank 0,1,-1 in rank column
countZero = 0
for i in df['Rank']:
    if i == 0:
        countZero += 1

countOne = 0
for i in df['Rank']:
    if i == 1:
        countOne += 1

countMinus = 0
for i in df['Rank']:
    if i == -1:
        countMinus += 1

print("Number of rank 0: ", countZero)
print("Number of rank 1: ", countOne)
print("Number of rank -1: ", countMinus)





