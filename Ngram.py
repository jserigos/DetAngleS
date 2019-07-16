import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix

def main():
    # sklearn
    target_csv = pd.read_csv('target_full_df.csv', encoding='utf-8')
    target_csv_df = pd.DataFrame(target_csv)
    print(len(target_csv_df))
    print(target_csv_df['Anglicism'].value_counts())


    target_label = target_csv_df["Anglicism"]
    print(target_label.shape)

    target_X = target_csv_df.drop(['Language', 'Anglicism'], axis=1)
    print(target_X.shape)
    X_train, X_test, y_train, y_test = train_test_split(target_X, target_label, test_size=0.5)
    '''
    vectorizer = CountVectorizer(ngram_range=(1,1))
    clf = LinearSVC()
    pipe = Pipeline([('vectorizer', vectorizer), ('clf', clf)])
    pipe.fit(X_train, y_train)

    y_predicted = pipe.predict(X_test)

    print(confusion_matrix(y_test, y_predicted))
    '''
if __name__ == '__main__':
    main()