# Using Python 3.6.5
import spacy
from spacy.tokens import Token
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
import re
import os

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

class tasi_text:
    def __init__(self, text):
        self.text = text
        self.spacy_text = self._spacy_setup()
        self._tag()

    def _spacy_setup(self): 
        nlp = spacy.load('es') # find how to disable syntactic parsing to speed up algorithm
        is_candidate_filter = lambda token: token.pos_ in ["VERB", "NOUN", "ADJ"] \
                                            and token.is_stop == False \
                                            and any({"@", "#"} & set(token.text)) == False
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
    

class decider:
    def __init__(self):
        ngram_weights = self._setup
    def _setup(self):
        ngram_weights
        look_up



def main(argv):
	tasi_text = tasi_text()
    if argv[0] == '-a':
        tasi_text.annotate(argv[1])
    elif argv[0] == '-e':
        tasi_text.evaluate(argv[1])
    else:
        tasi_text.annotate(argv[0])
        tasi_text.evaluate(argv[1])
    os.system('say "your program has finished"')

if __name__ == '__main__':
    setup_package()


"""
class tasi_doc:
    def __init__(self, text):
        self.text = text
        self.dataframe = self._dataSetUp()
        self.nlp = spacy.load('es', tag=True, entity=True, stop=True, disable=["textcat", "parser"])

    def _dataSetUp(self):
        nlp(text)

        return() 
"""