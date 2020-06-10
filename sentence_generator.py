from nltk.parse.generate import generate, demo_grammar
from nltk import CFG

grammar = CFG.fromstring(demo_grammar)
print(grammar)