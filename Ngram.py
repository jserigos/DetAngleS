import pandas as pd
import numpy as np
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


def main():
    target_csv = pd.read_csv('Data/target_full_df.csv', encoding='utf-8')
    target_csv_df = pd.DataFrame(target_csv)
    print(target_csv_df['Anglicism'].value_counts())

    target_label = target_csv_df["Anglicism"]

    target_X = target_csv_df["Token"]
    X_train, X_test, y_train, y_test = train_test_split(target_X, target_label, test_size=0.5)

    vectorizer = CountVectorizer(ngram_range=(1, 5), analyzer='char')

    # clfs = [LinearSVC(), MultinomialNB(), svm.SVC(kernel='linear'), SGDClassifier(loss='hinge',penalty='l2',alpha=1e-3, random_state=42)]
    pipe = Pipeline([('vectorizer', CountVectorizer(ngram_range=(1, 5), analyzer='char')),
                     ('tfidf', TfidfTransformer()),
                     ('clf', LinearSVC())])
    pipe.fit(X_train, y_train)

    y_predicted = pipe.predict(X_test)
    print(X_test.shape)
    print(y_test.shape)
    print(y_predicted.shape)
    print(classification_report(y_test, y_predicted, target_names=['FALSE', 'OTHER', 'TRUE']))
    print(confusion_matrix(y_test, y_predicted))
    print(accuracy_score(y_test, y_predicted))

    result_df = pd.DataFrame({'Token': X_test, 'label': y_test})
    result_df['predicted'] = y_predicted
    result_df.to_csv(r'Data/result_OpinionArticles_df.csv', index=None, header=True)
    print(result_df.shape)




if __name__ == '__main__':
    main()
