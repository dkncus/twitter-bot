from textblob import TextBlob
from textblob.taggers import NLTKTagger
import nltk

blob = TextBlob("", pos_tagger=NLTKTagger())
print(blob.pos_tags)