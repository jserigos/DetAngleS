from collections import defaultdict
import math
import re
import io
import os
import pkg_resources

resource_package = "anglicismIdentifier"  # Could be any module/package name

Eng_resource_path = '/'.join(['TrainingCorpora', 'EngDict.txt'])
EngPath = pkg_resources.resource_filename(resource_package, Eng_resource_path)
EngDict = io.open(EngPath, 'r', encoding='utf8').read().split("\n")

Spn_resource_path = '/'.join(['TrainingCorpora', 'lemario-20101017.txt'])
SpnPath = pkg_resources.resource_filename(resource_package, Spn_resource_path)
SpnDict = io.open(SpnPath, 'r', encoding='utf8').read().split("\n")

Spn_lemma_path = '/'.join(['TrainingCorpora','lemmatization-es.txt'])
SpnPath2 = pkg_resources.resource_filename(resource_package, Spn_lemma_path)
SpnLemmaList = io.open(SpnPath2, 'r', encoding='utf8').read().split("\n")

spLemmaDict = defaultdict(list)
for x in SpnLemmaList:
    try:
        a,b = x.split('\t')
        spLemmaDict[b].append(a)
    except ValueError:
        print x

class look_up:
    def __init__(self, spacy_text):
        self.spacy_text = spacy_text
        self._generateTags()


    def _generateTags(self):
        for k, word in enumerate(self.spacy_text):
            # determine NE
            if FILTER:
               # add "NAs" to new columns
                if engLemma not in EngDict or spnLemmaList:
                    self.lemmas.append("|".join(spnLemmaList))
                    self.lang.append("Spn")
                    self.ang.append("No")
                elif spnLemma in SpnDict:
                    self.lemmas.append(spnLemma)
                    self.lang.append("Spn")
                    self.ang.append("No")
                else:
                    self.lemmas.append(engLemma)
                    self.lang.append("Eng")
                    if NE == "0":
                        self.ang.append("Yes")
                    else:
                        self.ang.append("No")
         