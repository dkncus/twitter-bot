from textblob import TextBlob
from textblob.taggers import NLTKTagger
import nltk

blob = TextBlob("Dave peed on Hunter during TK.", pos_tagger=NLTKTagger())
print(blob.pos_tags)