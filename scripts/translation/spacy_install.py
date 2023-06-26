from preprocessing import *

# basic files
import time, os, json, os, math, string
from collections import Counter,OrderedDict
from typing import Any, Optional, Dict
from pprint import pprint
from tqdm import tqdm
# from tqdm import trange
# from tqdm.notebook import tqdm

import pandas as pd
import numpy as np

import torch
import torchtext as tt

import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language


import nltk 
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize

# spacy.cli.download("en_core_web_sm")
ner = spacy.load("en_core_web_sm")

def get_lang_detector(nlp, name):
    return LanguageDetector()

nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(f"Device: {device}")

def ProperNounExtractor(text):
    
    # print('PROPER NOUNS EXTRACTED :')
    words = nltk.word_tokenize(text)
    words = [word for word in words if word not in (set(stopwords.words('english')) and string.punctuation)]
    tagged = nltk.pos_tag(words)
    for (word, tag) in tagged:
        if tag == 'NNP' or tag == 'NNPS' or tag == 'NNS' or tag == 'NN': # If the word is a proper noun
            return True

        return False
