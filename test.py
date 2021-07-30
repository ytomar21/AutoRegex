import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_trf")
doc = nlp("Testing this text")

for tok in doc:
    print(f'Token: {tok}, Dependency: {tok.dep_}, Left Edge: {tok.left_edge}, Right Edge: {tok.right_edge}')

displacy.serve(doc, style='dep', options={'compact':True})
