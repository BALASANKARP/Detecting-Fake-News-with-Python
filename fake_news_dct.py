# -*- coding: utf-8 -*-
"""case2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ir6Oil0BK0TFKUwxwA1_G69rpPMBqpIs
"""

!pip install -q wordcloud
import wordcloud

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


import pandas as pd
train = pd.read_csv('/content/drive/MyDrive/train.csv')
train.head()

import nltk
nltk.download('stopwords')

from google.colab import drive
drive.mount('/content/drive')

# Firstly, fill all the null spaces with a space
train = train.fillna(' ')
train['total'] = train['title'] + ' ' + train['author'] + ' ' +train['text']

from ntlk.corpus import stopwords
from ntlk.stem import WordNetLemmatizer



stop_words = stopwords.words('english')



word_data = "It originated from the idea that there are readers who prefer learning new skills from the comforts of their drawing rooms"
nltk_tokens = nltk.word_tokenize(word_data)
print(nltk_tokens)

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

for index, row in train.iterrows():
    filter_sentence = ''
    sentence = row['total']
    # Cleaning the sentence with regex
    sentence = re.sub(r'[^\w\s]', '', sentence)
    # Tokenization
    words = nltk.word_tokenize(sentence)
    # Stopwords removal
    words = [w for w in words if not w in stop_words]
    # Lemmatization
    for words in words:
        filter_sentence = filter_sentence  + ' ' +str(lemmatizer.lemmatize(words)).lower()
    train.loc[index, 'total'] = filter_sentence
train = train[['total', 'label']]

X_train = train['total']
Y_train = train['label']

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
count_vectorizer = CountVectorizer()
count_vectorizer.fit_transform(X_train)
freq_term_matrix = count_vectorizer.transform(X_train)
tfidf = TfidfTransformer(norm = "l2")
tfidf.fit(freq_term_matrix)
tf_idf_matrix = tfidf.fit_transform(freq_term_matrix)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(tf_idf_matrix,
                                   Y_train, random_state=0)

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
Accuracy = logreg.score(X_test, y_test)
print(Accuracy*100)

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
Accuracy = clf.score(X_test, y_test)
print(Accuracy*100)

from sklearn.naive_bayes import MultinomialNB
NB = MultinomialNB()
NB.fit(X_train, y_train)
Accuracy = NB.score(X_test, y_test)
print(Accuracy*100)



