import spacy
import re
import markovify
import string
import random

def read_file(filepath):
    with open(filepath) as f:
        str_text = f.read()
    return str_text

while True:
    generated_file = open('generatedLines.txt', 'r+')
    generateLinesArr = generated_file.read().split('\n')
    cat_arr = ['academic','anti','boardgame','brand','character','classic','expression','fashion','food','health','holiday','music','objects','occupation','people','politics','religion','show','situation','sports','videogame','weather']
    ind = random.randint(0,len(cat_arr)-1)
    category = cat_arr[ind]
    file = f'{category}.txt'
    with open(file) as f:
        text = f.read()

    def text_cleaner(text):
        text = re.sub(r'--', ' ', text)
        text = re.sub('[\[].*?[\]]', '', text)
        text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
        text = ' '.join(text.split())
        return text

    text = text_cleaner(text)

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

    for i in range(10):
        isSentence = False
        while not isSentence:
            sentence = generator_2.make_sentence()
            if sentence != None:
                sent_arr = sentence.split(' ')
                answer = ''
                for word in sent_arr:
                    char_arr = [char for char in word]
                    hasPunc = False
                    for char in char_arr:
                        if char in string.punctuation:
                            hasPunc = True
                    if hasPunc:
                        answer = answer.rstrip(' ')
                        answer += f'{word} '
                    else:
                        answer += f'{word} '
                if answer.rstrip(' ') not in generateLinesArr:
                    answer = answer.rstrip(' ') + '\n'
                    generated_file.write(answer)
                isSentence = True
        print('Line written')