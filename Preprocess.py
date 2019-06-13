# Using Python 3.6.5
# TO DO 
    ## Note multi-word anglicisms as a unit with I,O,B tagging

import spacy
from spacy.tokens import Token
from spacy.tokenizer import Tokenizer
from spacy.util import compile_prefix_regex, compile_infix_regex, compile_suffix_regex
import re
import os
import io
 
class tasi_text:
    def __init__(self, text):
        self.spacy_text = nlp(text)
        self._tag()

    def _tag(self):
        for token in self.spacy_text:
            if token._.is_candidate == True:
                # send to main module
                if len(token) > 5:
                    token._.is_anglicism = True

    def anglicisms(self):  # return list of anglicisms
        return [token for token in self.spacy_text if token._.is_anglicism]
    
    def annotate_to_csv(self, output_file_path):  # write to output file
        with io.open(output_file_path, 'w', encoding='utf8') as output:
            output.write(u"Token\tLemma\tPOS\tLanguage\tCandidate\tAnglicism\n")
            for token in self.spacy_text:
                output.write("\t".join([token.text, token.lemma_, token.pos_, str(token._.is_candidate), str(token._.is_anglicism), "\n"]))

    def evaluate(self, gold_standard):
        # compare to gold standard 
        return "in progress"
    
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

def spacy_setup(): 
    nlp = spacy.load('es') # find how to disable syntactic parsing to speed up algorithm
    is_candidate_filter = lambda token: token.pos_ in ["VERB", "NOUN", "ADJ"] \
                                            and token.is_stop == False \
                                            and any({"@", "#"} & set(token.text)) == False
    Token.set_extension("is_candidate", getter=is_candidate_filter)
    Token.set_extension("is_anglicism", default=False)
    nlp.tokenizer = custom_tokenizer(nlp)
    return nlp


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
    nlp = spacy_setup()

text1 = """El médico argentino Eduardo Sosa en el hat-trick de su twitter @yesyes y #happy en https://www.lanacion.com.ar/e y su esposa Edith gat@gmail.com fueron a dejar todo en la Argentina para mudarse con su familia a Bielorrusia, la ex república de la Unión Soviética que había sufrido las mayores consecuencias de la explosión de la central de Chernobyl, ubicada a pocos kilómetros de la frontera con Ucrania. """
text2 = """El médico argentino Eduardo Sosa en hat-trick de su twitter @yesyes y #happy"""
sample1 = tasi_text(text1)
sample2 = tasi_text(text2)