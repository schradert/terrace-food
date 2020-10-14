###########################
### IMPORTS & CONSTANTS ###
###########################

import json
import re
import nltk
# nltk.download()   # necessary for English corpora
import pandas as pd
import numpy as np
from pprint import pprint

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.chunk import ne_chunk

STOPWORDS = set(stopwords.words('english'))
MEALTYPES = ('soup', 'entree', 'side', 'dessert')

####################
### DATA LOADING ###
####################

with open('menus/data.json') as f:
    data = json.load(f)

names = {
    type_: [dish['name'].lower()\
            for day in data\
            for dish in day['dishes']\
            if dish['type'] == type_]\
    for type_ in MEALTYPES}
tokens = {
    type_: [word_tokenize(name) for name in nameset]\
    for type_, nameset in names.items()}
filtered = {
    type_: [' '.join([token\
                      for token in tokens_\
                      if token not in STOPWORDS])\
            for tokens_ in tokenset]\
    for type_, tokenset in tokens.items()}
freqs = {
    type_: nltk.FreqDist(filterset)\
    for type_, filterset in filtered.items()}
tagged = {
    type_: [pos_tag(tokens_) for tokens_ in tokenset]\
    for type_, tokenset in tokens.items()}
themes = [day['theme']\
          for day in data\
          if 'theme' in day.keys()]

#################
### FUNCTIONS ###
#################

def print_commons(freqs_):
    for type_, freqdist in freqs_.items():
        print(f'{type_.capitalize()}s')
        pprint(freqdist.most_common(15))

def extract(tree, *, phrase=False):
    return [subtree.leaves()[0][0]\
            if not phrase\
            else ' '.join([leaf[0]\
                           for leaf in subtree.leaves()])\
            for subtree in tree\
            if not isinstance(subtree, tuple)]

def parse_pos(gram, *, phrase=False):
    parser = nltk.RegexpParser(gram)
    parsed = {
        type_: [word\
                for tags in tagset\
                for word in extract(
                    parser.parse(tags),
                    phrase=phrase)]\
        for type_, tagset in tagged.items()}
    parsed_freqs = {
        type_: nltk.FreqDist(parseset)\
        for type_, parseset in parsed.items()}
    return parsed, parsed_freqs

####################
### MAIN PARSING ###
####################

adj_gram = r'''ADJ: {<JJ.?|VBD|VBG>}'''
adjectives, adjectives_freqs = parse_pos(adj_gram)
noun_gram = r'''Noun: {<NN|NNS|NNP|NNPS>}'''
nouns, nouns_freqs = parse_pos(noun_gram)
np1_gram = r'''NP: {<NN|NNS|NNP|NNPS>+}'''
nps1, nps1_freqs = parse_pos(np1_gram, phrase=True)
np2_gram = r'''NP: {<NN|NNS|NNP|NNPS>{2,}}'''
nps2, nps2_freqs = parse_pos(np2_gram, phrase=True)

print('---- Most Common (Dishes) ----')
print_commons(freqs)
print('---- Most Common (Themes) ----')
pprint(nltk.FreqDist(themes).most_common())
print('---- Most Common (Adjectives) ----')
print_commons(adjectives_freqs)
print('---- Most Common (Nouns) ----')
print_commons(nouns_freqs)
print('---- Most Common (Noun Phrases 1+) ----')
print_commons(nps1_freqs)
print('---- Most Common (Noun Phrases 2+) ----')
print_commons(nps2_freqs)


graph_data = {
    'dishes': {k:v.most_common() for k,v in freqs.items()},
    'themes': nltk.FreqDist(themes).most_common(),
    'adjs': {k:v.most_common() for k,v in adjectives_freqs.items()},
    'nouns': {k:v.most_common() for k,v in nouns_freqs.items()},
    'noun_phrases_1+': {k:v.most_common() for k,v in nps1_freqs.items()},
    'noun_phrases_2+': {k:v.most_common() for k,v in nps2_freqs.items()},
}

with open('menus/graph_data.json', 'w') as f:
    json.dump(graph_data, f, indent=4)