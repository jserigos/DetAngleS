import pandas as pd
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix


def main():
    output = []

    # Samples to run in python console or testing
    with open('target_token.txt', encoding="utf8") as word_list:
        # read the contents into the words list using list comprehension
        words = [word.strip().lower() for word in word_list]

    with open('NACC-GoldStandard.tsv', encoding="utf8") as tsv:
        # read the contents of stuff.tsv into the line list using list comprehension
        lines = [line for line in tsv]

    # iterate over the lines
    for line in lines:

        # iterate over the word list
        for word in words:

            # if we find one of the words in the line, then add it to the output list
            if word in line.lower():

                # if the TSV line doesn't end with a newline character, insert one
                if line.endswith('\n'):
                    output.append(line)
                else:
                    output.append('{0}\n'.format(line))

    # dropping duplicate rows
    output = list(dict.fromkeys(output))

    # open output.tsv using a with block with write permissions
    with open('output.tsv', 'w', encoding="utf8") as output_file:

        # write the output list to the file
        output_file.writelines(output)

    # sklearn
    target_tsv = pd.read_csv('output.tsv', delimiter='\t', encoding='utf-8', header=0)
    target_tsv_df = pd.DataFrame(target_tsv)
    print(len(target_tsv_df))
    target_csv = pd.read_csv('target_token_df.csv', encoding='utf-8')
    target_csv_df = pd.DataFrame(target_csv)
    print(len(target_csv_df))
    target_full_df = target_tsv_df.merge(target_csv_df, left_on='Token', right_on='Token')
    target_full_df.drop_duplicates(keep=False, inplace=True)
    print(len(target_full_df))

    target_full_df.to_csv(r'target_df.csv', index=None, header=True)
    '''
    target_X = target_full_df.drop('Anglicism', axis=1)
    target_label = target_full_df['Anglicism']
    X_train, X_test, y_train, y_test = train_test_split(target_X, target_label, test_size=0.2)


    vectorizer = CountVectorizer(ngram_range=(1,1))
    clf = LinearSVC()
    pipe = Pipeline([('vectorizer', vectorizer), ('clf', clf)])
    pipe.fit(X_train, y_train)

    y_predicted = pipe.predict(X_test)

    print(confusion_matrix(y_test, y_predicted))
        
    '''
if __name__ == '__main__':
    main()