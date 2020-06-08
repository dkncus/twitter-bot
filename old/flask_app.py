from flask import Flask
import markov_chain
import random

h = list(markov_chain.get_dict('words.txt'))

app = Flask(__name__)

@app.route('/')

def hello_world():
	return h[random.randint(0, len(h))]