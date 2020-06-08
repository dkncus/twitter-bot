from flask import Flask
import textgen

words = textgen.get_dict('words.txt')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return textgen.print_sentence(words, 8)