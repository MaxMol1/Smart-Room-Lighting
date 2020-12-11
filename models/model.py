import pandas as pd

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report

def process_data():
    df = pd.read_json('./reviews_Digital_Music_5.json', lines=True)
    df.drop(['reviewerID', 'asin', 'reviewerName', 'helpful', 'summary', 'unixReviewTime', 'reviewTime'], axis=1, inplace=True)

    # TODO: MinMaxScalar
    
    nltk.download('punkt')
    nltk.download('stopwords')

    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = stopwords.words('english') + list(string.punctuation)
    stop_words += ["ve", "nt", "s", "d", "ll", "re", "m"]

    # Remove tags, links, hashtags ..?
    df['reviewText'] = df.apply(lambda row : ' '.join(w for w in row['reviewText'].split(' ') if not w.startswith('@') and not w.startswith('http')), axis = 1)
    # Tokenize, remove punctuation, stopwords, numbers
    df['reviewText'] = df.apply(lambda row : tokenizer.tokenize(row['reviewText'].lower()), axis = 1)
    df['reviewText'] = df.apply(lambda row : [w for w in row['reviewText'] if not w in stop_words or not w.isnumeric()], axis = 1)
    # Join list of words into one string
    df['review_full'] = df.apply(lambda row : " ".join(row['reviewText']), axis = 1)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['review_full'])
    y = df['overall']

    # Split data 80:20 with shuffling
    return train_test_split(X, y, test_size=0.2, shuffle=True, random_state=3)

def create_model(X_train, X_test, y_train, y_test):
    clf = OneVsRestClassifier(LogisticRegressionCV(cv=2, Cs=[100]))
    clf.fit(X_train, y_train)

    # Gather predictions for Y
    y_pred = clf.predict(X_test)

    # Print Classification report
    report = classification_report(y_test, y_pred, output_dict = True)
    pd.DataFrame(report)

def main():
    print ("Processing data ...")
    X_train, X_test, y_train, y_test = process_data()
    print ("Creating model ...")
    create_model(X_train, X_test, y_train, y_test)
    print ("Done!")
    
if __name__ == "__main__":
    main()
