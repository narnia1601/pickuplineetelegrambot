import spacy
import re
import nltk
import markovify

def read_file(filepath):
    with open(filepath) as f:
        str_text = f.read()
    return str_text

nlp = spacy.load('en_core_web_sm', disable=['parser','tagger','ner'])

def separate_punc(doc_text):
    return [token.text.lower() for token in nlp(doc_text)]

text = read_file('Holidayfile.txt')

def text_cleaner(text):
    text = re.sub(r'--', ' ', text)
    text = re.sub('[\[].*?[\]]', '', text)
    text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
    text = ' '.join(text.split())
    return text

nlp = spacy.load('en_core_web_sm')
text_doc = nlp(text)
text_sents = ' '.join([sent.text for sent in text_doc.sents if len(sent.text) > 1])

generator_1 = markovify.Text(text_sents, state_size=4)
class POSifiedText(markovify.Text):
   def word_split(self, sentence):
      return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
   def word_join(self, words):
      sentence = ' '.join(word.split('::')[0] for word in words)
      return sentence
generator_2 = POSifiedText(text_sents, state_size=4)

for i in range(5):
  print(generator_2.make_sentence())
