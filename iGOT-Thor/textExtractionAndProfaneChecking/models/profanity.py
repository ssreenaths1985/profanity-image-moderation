# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import json
import re
import time

from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

import textacy
import spacy
import time 



last_timestamp = time.time()
from textExtractionAndProfaneChecking.models.context import getNlp, getCustopProfanityList, getSvmClassifier, getCustopProfanityCategorical
def lineAnalysis(original_text, classifier):
        jobs   = []
        result = []
        with ThreadPoolExecutor(5) as executor:
            for line in original_text.split('.'):
                if line.strip():
                    jobs.append(executor.submit(classifier.predict, line))
                    #analysis = classifier.predict(line)
            for job in futures.as_completed(jobs):
                analysis = job.result()
                obj = {}
                obj['line'] = analysis['text']
                obj['classification'] = analysis['classification']
                obj['probability'] = analysis['probability']
                result.append(obj)
        return result
def filter_and_tag(text):
    # print('started text analysis. timestamp:' + str(time.time()))
    last_timestamp = time.time()
    report = []
    original_text = text
    text = text.lower()
    # print('incoming---->' + str(text[0:10]) + '...')
    #for line in text.split('.'):
    if original_text.strip():
        nlp = getNlp()
        doc = nlp(original_text)
        spacy_analysis_time = time.time() - last_timestamp
        # print('spacy analysis done:' + str(spacy_analysis_time))
        ngrams3 = textacy.extract.ngrams(doc, 3)
        ngrams2 = textacy.extract.ngrams(doc, 2)
        ngrams = []
        ngrams.append(list(ngrams2))
        ngrams.append(list(ngrams3))

        offensiveWordDict = dict()
        # print("heyyy")
        custom_p = getCustopProfanityList()
        profanityCategoricalList = getCustopProfanityCategorical()
        offensiveWordDict, report, text = wordAnalysisCategorical(profanityCategoricalList, report, doc, text)
        
    word_analysis_time = time.time() - last_timestamp
    # print('completed word analysis. time taken in seconds:' + str(word_analysis_time) )
    last_timestamp = time.time()
    #frequency object
    frequency = []
    for key, value in offensiveWordDict.items():
        frequency.append({"word" : key, "no_of_occurrence" : value['count']})
    result = {}
    result['possible_profanity_categorical'] = offensiveWordDict
    result['possible_profanity'] = list(set(report))
    result['possible_profanity_frequency'] = frequency
    result['possible_profane_word_count'] = len(result['possible_profanity'])
    result['text_tagged'] = text
    result['text_original'] = original_text

    classifier = getSvmClassifier()
    result['overall_text_classification'] = classifier.predict(original_text)
    overall_text_classification_time = time.time() - last_timestamp
    # print('completed overall text analysis. time taken in seconds:' + str(overall_text_classification_time) )
    last_timestamp = time.time()
    result['line_analysis'] = {}
    if '.' in original_text:
        result['line_analysis'] = lineAnalysis(original_text, classifier)

    line_analysis_time = time.time() - last_timestamp
    # print('completed line wise text analysis. time taken in seconds:' + str(line_analysis_time) )

    result['performance'] = {'spacy_word_analysis_time_taken' : word_analysis_time,'custom_model_overall_text_classification_time_taken' : overall_text_classification_time, 'custom_model_line_analysis_time_taken' : line_analysis_time, 'num_lines' : len(original_text.split('.')) , 'num_words' : len(original_text.split()) }

    return result

def wordAnalysisCategorical(profanityCategoricalList, report, doc, text):
    # print('wordAnalysisCategorical')
    offensiveWordDict = dict()
    text = re.sub('\s+',' ',text)
    for profanity in profanityCategoricalList.keys():
        # print(profanity)
        # print(text)
        profanity_re = r"(\b)" + profanity + r"(\b)"
        # print(re.search(profanity_re, text))

        if re.search(profanity_re, text):
            offensiveWordDict[profanity] = {'count' : len(re.findall(profanity_re, text)), 'details' : profanityCategoricalList[profanity], 'classifier' : 'dictionary'}
            text = re.sub(profanity_re, '[' + profanity + '](possible profanity)', text)
            report.append(profanity)
            

    for token in doc:
            if token._.is_profane:
                if (token._.original_profane_word not in offensiveWordDict.keys()):
                    report.append(token._.original_profane_word)
                    offensiveWordDict[token._.original_profane_word] = {'count' : 1, 'details' : {"offensive": "severe"}, 'classifier' : 'NLP'}
                    profanity_re = r"(\b)" + token._.original_profane_word + r"(\b)"
                    text = re.sub(profanity_re, '[' + token._.original_profane_word + '](possible profanity)', text)
                elif 'NLP' in offensiveWordDict[token._.original_profane_word]['details'].keys():
                    profanityObj = offensiveWordDict[token._.original_profane_word]
                    profanityObj['count'] += 1
                    offensiveWordDict[token._.original_profane_word] = profanityObj
            # print('>>>' + text)
                
    return offensiveWordDict, report, text
