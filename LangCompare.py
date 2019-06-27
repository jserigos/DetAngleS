import spacy

nlp = spacy.load('es')
nlp_en = spacy.load('en')
   
def classify(spacy_token):
    Sp_Status = spacy_token.text in nlp.vocab
    En_Status= spacy_token.text in nlp_en.vocab
    if En_Status and not Sp_Status:
        return True
    else:
        return False
