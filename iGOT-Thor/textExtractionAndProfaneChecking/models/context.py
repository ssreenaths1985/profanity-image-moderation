from profanity_filter import ProfanityFilter
import spacy
from textExtractionAndProfaneChecking.models.offensive_model import SvmClassifier

import time
import os
import json


nlp = spacy.load('en')
profanity_filter = ProfanityFilter(nlps={'en': nlp})
#custom profanities
custom_p = json.load(open('textExtractionAndProfaneChecking/models/data/custom_profanity.json'))
custom_p_set = set()
for profanity in custom_p:
    custom_p_set.add(profanity)


profanity_filter.extra_profane_word_dictionaries = {'en' : custom_p_set}

profanity_filter_custom = ProfanityFilter()
profanity_filter_custom.extra_profane_word_dictionaries = {'en' : custom_p_set}

nlp.add_pipe(profanity_filter.spacy_component, last=True)

classifier = SvmClassifier()

categorical_custom_p = {}
profanityCategoricalList = {}
if os.path.exists('textExtractionAndProfaneChecking/models/data/custom/profanities.json'):
        fle = open('textExtractionAndProfaneChecking/models/data/custom/profanities.json', 'r+')
        profaniyList = fle.read()
        profanityCategoricalList = json.loads(str(profaniyList))

def refreshCustomProfanity():
    nlp = spacy.load('en')
    profanity_filter = ProfanityFilter(nlps={'en': nlp})
    #custom profanities
    custom_p = json.load(open('textExtractionAndProfaneChecking/models/data/custom_profanity.json'))
    custom_p_set = set()
    for profanity in custom_p:
        custom_p_set.add(profanity)

    profanity_filter.extra_profane_word_dictionaries = {'en' : custom_p_set}

    profanity_filter_custom = ProfanityFilter()
    profanity_filter_custom.extra_profane_word_dictionaries = {'en' : custom_p_set}

    nlp.add_pipe(profanity_filter.spacy_component, last=True)
    #refresh categorical profanities
    if os.path.exists('textExtractionAndProfaneChecking/models/data/custom/profanities.json'):
        fle = open('textExtractionAndProfaneChecking/models/data/custom/profanities.json', 'r+')
        profaniyList = fle.read()
        profanityCategoricalList = json.loads(str(profaniyList))
    return nlp

def refreshSvmClassifier():
    for fle in os.listdir('model'):
       os.rename("model/" + str(fle), "model_backup/" + str(fle) + '_' + str(time.time()))
    classifier = SvmClassifier()
    return classifier

def getSvmClassifier():
    return classifier

def getNlp():
    return nlp

def getCustopProfanityList():
    return custom_p

def getCustopProfanityCategorical():
    return profanityCategoricalList