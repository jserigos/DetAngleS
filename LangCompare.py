import spacy

nlp = spacy.load('es')
nlp_en = spacy.load('en')


## Lemmas can be reassigned token.lemma = "afueraspacy"
   
def classify(token):
    Sp_Status = token in nlp.vocab
    En_Status= token in nlp_en.vocab
    if En_Status and not Sp_Status:
        return True
    else:
        return False

