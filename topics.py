from pickletools import optimize
from tabnanny import verbose
from keras.preprocessing.text import Tokenizer
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, GRU, Dropout, Input
from pickle import dump,load
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import random
from sklearn.model_selection import train_test_split
import markovify
from keras.optimizers import Adam
import spacy

def read_file(filepath):
    with open(filepath) as f:
        str_text = f.read()
    return str_text

def separate_punc(text):
    word_arr = []
    word = ''
    for char in text:
        if char.isalpha():
            word += char.lower()
        if char == "'" and word != '' or char == '-' and word != '':
            word += char
        elif char == '\n':
            if word != '':
                word_arr.append(word)
                word = ''
            word_arr.append('\n')
        elif char == ' ' and word != '':
            word_arr.append(word)
            word = ''
    return word_arr

text = read_file('linefile.txt')
text = text[:300000]

tokens = separate_punc(text)

text_sequences = []

i = 0
sentence = ''
while i < len(tokens):
    if tokens[i] != '\n':
        sentence += f' {tokens[i]}'
    else:
        sentence = sentence.lstrip(' ')
        text_sequences.append(sentence)
        sentence = ''
    i += 1

phrase_sequences = []
for sentence in text_sequences:
    counter = 0
    firstWord = 0
    phrase_length = 3
    phrase = []
    sentence_arr = sentence.split(' ')
    while (firstWord + phrase_length) <= len(sentence_arr):
        for i in range(firstWord, firstWord+phrase_length):
            phrase.append(sentence_arr[i])
        phrase_sequences.append(phrase)
        phrase = []
        firstWord += 1

nlp = spacy.load('en_core_web_sm')

generator_1 = markovify.Text(text_sequences, state_size=4)
class POSifiedText(markovify.Text):
   def word_split(self, sentence):
      return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
   def word_join(self, words):
      sentence = ' '.join(word.split('::')[0] for word in words)
      return sentence
generator_2 = POSifiedText(text_sequences, state_size=4)

markovDone = False
while markovDone != True:
    sentence = generator_2.make_sentence()
    if sentence != None:
        sent_arr = sentence.split(' ')
        seed_text = (' '.join(sent_arr[:4]))
        markovDone = True

tokenizer = Tokenizer()
tokenizer.fit_on_texts(phrase_sequences)
sequences = tokenizer.texts_to_sequences(phrase_sequences)
vocabulary_size = len(tokenizer.word_counts) + 1
sequences = np.array(sequences)

X = sequences[:,:-1]
y = sequences[:,-1]
y = to_categorical(y,num_classes=vocabulary_size)

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=42)

seq_len = X.shape[1]

model = Sequential()
model.add(Embedding(vocabulary_size,seq_len,input_length=seq_len))
model.add(LSTM(100,return_sequences=True))
model.add(Dropout(0.1))
model.add(GRU(100))
model.add(Dropout(0.1))
model.add(Dense(vocabulary_size,activation='softmax'))
adam = Adam(0.001)
model.compile(optimizer=adam, loss='categorical_crossentropy')

model.fit(X_train,y_train,epochs=600, batch_size=32,verbose=1)

def generate_text(model,tokenizer,seq_len,seed_text,num_gen_words):
    output_text = []
    input_text = seed_text
    for i in range(num_gen_words):
        encoded_text = tokenizer.texts_to_sequences([input_text])[0]
        pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')
        pred_word_ind = model.predict_classes(pad_encoded, verbose=0)[0]
        pred_word = tokenizer.index_word[pred_word_ind]
        input_text += ' ' + pred_word
        output_text.append(pred_word)
    answer = ' '.join(output_text)
    answer = seed_text + answer
    return answer

print(generate_text(model,tokenizer,seq_len,seed_text,10))