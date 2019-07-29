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
import subprocess


# this version still leaves extra whitespace, not sure why
def cleanText_new(text):
    # get rid of newlines
    regex = r"\s\s+|\n|\r"
    subst = " "
    cleaned = re.subn(regex, subst, text, re.MULTILINE)
    return cleaned

# clean text before spacy
def cleanText(text):
    # get rid of newlines
    text = text.strip().replace("\n", " ").replace("\r", " ").replace("\r\n", " ").replace("  ", " ")
    return text

# deal with more symbols to seperate tokens
# deal with url and hashtag
def custom_tokenizer_modified(nlp):
    # spacy defaults: when the standard behaviour is required, they
    # need to be included when subclassing the tokenizer
    infix_re = re.compile(r'''[.\,\?\!\:\...\‘\’\`\“\”\"\'\/~]''')
    extended_prefixes = tuple(list(nlp.Defaults.prefixes) + ["-"])
    prefix_re = compile_prefix_regex(extended_prefixes)
    extended_suffixes = tuple(list(nlp.Defaults.suffixes) + ["-"])
    suffix_re = compile_suffix_regex(extended_suffixes)

    # extending the default url regex with regex for hashtags with "or" = |
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
            df.loc[i, 'Language'] = "Stop Word"
            df.loc[i, 'Anglicism'] = "No"
        # Ignore NEs
        elif(df.loc[i,'NE'] != "O"):
            df.loc[i, 'Language'] = "Name Entity"
            df.loc[i, 'Anglicism'] = "No"
    return df


def main():
    # Default read text in spanish
    nlp = spacy.load('es_core_news_sm')

    # Tokenize text using custom tokenizer
    nlp.tokenizer = custom_tokenizer_modified(nlp)

    # Samples to run in python console or testing

    text = open("Data/OpinionArticles-text.txt", encoding="utf8").read()
    #text1 = open("Sample.txt").read()

    # clean text
    clean_text = cleanText(text)

    # spacy text
    doc = nlp(clean_text)

    # update user on length of tokens
    print("Processing %s word document" %len(doc))

    # write token into data frame
    text_df = custom_tokenizer_to_df(doc)

    # Filter out non interested tokens by assigning label
    filter_noninterested_text(nlp, text_df)

    # write df to csv
    text_df.to_csv(r'Data/OpinionArticles-TASI.csv', index=None, header=True)

    #open annotated file
    subprocess.call(['open',r'Data/OpinionArticles-TASI.csv'])


if __name__ == '__main__':
    main()