# Using Python 3.6.5
# TO DO
## Note multi-word anglicisms as a unit with I,O,B tagging
import pandas as pd
import numpy as np
import spacy
from spacy.tokens import Token
from spacy.tokenizer import Tokenizer
from spacy.lang.tokenizer_exceptions import URL_PATTERN
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
import re

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics



# create a custom tokenizer that keep hypen words together ex. hat-trick
# and keeps hashtag symbol together with its word ex. #yolo
def custom_tokenizer(nlp):
    infix_re = re.compile(r'''[\,\?\;\‘\’\`\“\”\"\'~]''')
    modified_prefixes = tuple(x for x in nlp.Defaults.prefixes if x != '#')
    prefix_re = compile_prefix_regex(modified_prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    is_candidate_filter = lambda token: token.pos_ in ["VERB", "NOUN", "ADJ"] and (token.is_stop == False) and (any(
        {"@", "#"} & set(token.text)) == False)
    Token.set_extension("is_candidate", getter=is_candidate_filter, force=True)
    Token.set_extension("is_anglicism", default=False, force=True)
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=None)


# deal with more symbols to seperate tokens
# deal with url and hashtag
def custom_tokenizer_modified(nlp):
    # spacy defaults: when the standard behaviour is required, they
    # need to be included when subclassing the tokenizer
    infix_re = re.compile(r'''[.\,\?\!\:\;\...\‘\’\`\“\”\"\'~]''')
    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)

    # extending the default url regex with regex for hashtags
    hashtag_pattern = r'''|^(#[\w_-]+)$'''
    url_and_hashtag = URL_PATTERN + hashtag_pattern
    url_and_hashtag_re = re.compile(url_and_hashtag)

    # set a custom extension to match if token is a hashtag
    hashtag_getter = lambda token: token.text.startswith('#')
    Token.set_extension('is_hashtag', getter=hashtag_getter, force=True)

    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                     suffix_search=suffix_re.search,
                     infix_finditer=infix_re.finditer,
                     token_match=url_and_hashtag_re.match
                     )


# write all the tokens extracted from text into a data frame
def custom_tokenizer_to_df(doc):

    # Write the tokens to data frame
    df = pd.DataFrame()
    df["Token"] = [token.text for token in doc]
    df["Language"] = np.nan
    df["POS"] = [token.pos_ for token in doc]
    df["NE"] = [token.ent_iob_ for token in doc]
    df["Lemma"] = [token.lemma_ for token in doc]
    df["Anglicism"] = np.nan
    return df


# filter out non interested text by three criteria below
def filter_noninterested_text(nlp, df):
    for i in df.Token.index:
        # Ignore any POS tags that are not Noun, VERB, or Adjective
        if(df.loc[i,"POS"] not in ["NOUN", "VERB", "ADJ"]):
            df.loc[i, 'Language'] = df.loc[i,'POS']
            df.loc[i, 'Anglicism'] = "No"
        # Ignore Stop Words
        elif(nlp.vocab[df.loc[i,'Token']].is_stop):
            df.loc[i, 'Language'] = "stop word"
            df.loc[i, 'Anglicism'] = "No"
        # Ignore NEs
        elif(df.loc[i,'NE'] != "O"):
            df.loc[i, 'Language'] = "name entity"
            df.loc[i, 'Anglicism'] = "No"

    return df


def main():
    # Default read text in spanish
    nlp = spacy.load('es_core_news_sm')

    # Tokenize text using custom tokenizer
    nlp.tokenizer = custom_tokenizer_modified(nlp)

    # Samples to run in python console or testing
    text1 = u"""El médico argentino Eduardo Sosa en el hat-trick de su twitter @yesyes y #happy en 
          https://www.lanacion.com.ar/e y su esposa Edith gat@gmail.com fueron a dejar todo en la Argentina para mudarse con su 
          familia a Bielorrusia, la ex república de la Unión Soviética que había sufrido las mayores consecuencias de la 
          explosión de la central de Chernobyl, ubicada a pocos kilómetros de la frontera con Ucrania. """
    doc = nlp(text1)

    # write token into data frame
    NACC_df = custom_tokenizer_to_df(doc)

    # Filter out non interested tokens by assigning label
    filter_noninterested_text(nlp, NACC_df)

    NACC_df.to_csv(r'spacy-annotated_df.csv', index=None, header=True)



if __name__ == '__main__':
    main()
