import spacy
from spacy.tokens import Token
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
import re
import os

##### TO DO --> filter out internet jargon (websites, hashtags, twitter handles)

# create a custom tokenizer that keep hypen words together ex. hat-trick
# and keeps hashtag symbol together with its word ex. #yolo
def custom_tokenizer(nlp):
    infix_re = re.compile(r'''[\,\?\;\‘\’\`\“\”\"\'~]''')
    modified_prefixes = tuple(x for x in nlp.Defaults.prefixes if x != '#')
    prefix_re = compile_prefix_regex(modified_prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                            token_match=None)
def is_candidate_filter(token): 
    if token.pos_ in ["VERB", "NOUN", "ADJ"] and token.is_stop == False: # include PROPN?
        if any({"@", "#"} & set(token.text)):
            return False
        else:
            return True


class tasi_text:
    def __init__(self, text):
        self.text = text
        self.spacy_text = self._spacy_setup()
        self._tag()

    def _spacy_setup(self): 
        nlp = spacy.load('es') # find how to disable syntactic parsing to speed up algorithm
        is_candidate_filter = lambda token: token.pos_ in ["VERB", "NOUN", "ADJ"] and token.is_stop == False and any({"@", "#"} & set(token.text)) == False# include PROPN?
        Token.set_extension("is_candidate", getter=is_candidate_filter)
        Token.set_extension("is_anglicism", default=False)
        nlp.tokenizer = custom_tokenizer(nlp)
        return nlp(self.text)
    
    def _tag(self):
        for token in self.spacy_text:
            if token._.is_candidate == True:
                # send to main module
                if len(token) > 5:
                    token._.is_anglicism = True
        for token in self.spacy_text:
            print(token.text, token.lemma_, token.pos_, token._.is_candidate, token._.is_anglicism) 

    def anglicisms(self):
        # return list of anglicisms
        return [token for token in self.spacy_text if token._.is_anglicism]
    
    def annotate(self, output_file_path):
        # write to output file
        return "in progress"

    def evaluate(self, gold_standard):
        self.tag(spacy_text)
        # compare to gold standard 
        return "in progress"
    

text1 = """El médico argentino Eduardo Sosa en el hat-trick de su twitter @yesyes y #happy en https://www.lanacion.com.ar/e y su esposa Edith gat@gmail.com fueron a dejar todo en la Argentina para mudarse con su familia a Bielorrusia, la ex república de la Unión Soviética que había sufrido las mayores consecuencias de la explosión de la central de Chernobyl, ubicada a pocos kilómetros de la frontera con Ucrania. """
text2 = """El médico argentino Eduardo Sosa en hat-trick de su twitter @yesyes y #happy"""
sample = tasi_text(text1)
print(sample.anglicisms())
"""
doc = nlp(text)
for token in doc:
    print(token)
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_alpha, token.is_stop, token._.is_candidate)


   return() 
"""