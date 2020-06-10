from flask import Flask
import textgen
from markov_chain import MarkovChain

words = textgen.get_dict('words.txt')

app = Flask(__name__)


m = MarkovChain('holmes.txt')
'''
for n in m.markov_chain:
	print(n)
	print('\t', m.markov_chain[n])
'''

print(m.walk(12, "clay"))

@app.route('/')
def hello_world():
    return textgen.print_sentence(words, 8)

if __name__ == '__main__':
    app.run()