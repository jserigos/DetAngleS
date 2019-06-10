# Using Python 3.6.5
import spacy
import os

class tasi_text:
    def __init__(self, text):
        self.spacy_text = self._setup()
        self.text = text

    def _setup(self):
    	nlp_sp = spacy.load('es', tag=True, entity=True, stop=True, disable=["textcat", "parser"])
    	return nlp_sp(text)
  	
  	def tag(self, text):
        
        return annotated_text

	def annotate(self, text):


	def evaluate(self, gold_standard):



def main(argv):
	tasi_text = tasi_text()
    if argv[0] == '-a':
        tasi_text,annotate(argv[1])
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
        self.nlp_sp = spacy.load('es', tag=True, entity=True, stop=True, disable=["textcat", "parser"])

    def _dataSetUp(self):
        nlp_sp(text)

        return() 
"""