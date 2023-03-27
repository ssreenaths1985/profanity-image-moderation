# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd
from sklearn.svm import SVC
import scipy
from sklearn.utils import shuffle
import pickle
from os import path

# from bert_serving.client import BertClient



class SvmClassifier:

    global vectorizer
    global clf
    global bClient

    def __init__(self,data=None):
        if data is None:
            if path.exists('textExtractionAndProfaneChecking/models/model/model.sav') and path.exists('textExtractionAndProfaneChecking/models/model/vectorizer.pk'):
                self.clf = pickle.load(open('textExtractionAndProfaneChecking/models/model/model.sav', 'rb'))
                self.vectorizer = pickle.load(open('textExtractionAndProfaneChecking/models/model/vectorizer.pk', 'rb'))
            else:
                csv = pd.read_csv('textExtractionAndProfaneChecking/models/data/consolidated_data.csv')
                csv = shuffle(csv)
                csv = csv.head(20000)
                data = pd.DataFrame()
                data['is_offensive'] = csv['is_offensive']
                data['text'] = csv['text']
                self.train_model(data)
                #self.bClient = BertClient()
        else:
            self.train_model(data)

    def train_model(self, data):
        result = pd.DataFrame()
        data = data.dropna()
        result['is_offensive'] = data['is_offensive']
        self.vectorizer = TfidfVectorizer(stop_words='english').fit(data['text'])

        tf = self.vectorizer.transform(data['text'])

        # print('result.shape' + str(result.shape))
        # print('data[text]' + str(data['text'].shape))
        tf_test = tf[int(result.shape[0] - result.shape[0]/5):]
        tf_train = tf[:int(result.shape[0] - result.shape[0]/5)]
        result_train = result.head(int(result.shape[0] - result.shape[0]/5))
        result_test  = result.tail(int(result.shape[0]/5) +1)
        # print(tf_train.shape)
        # print(result_train.shape)
        # print(tf_test.shape)
        # print(result_test.shape)
        self.clf = SVC(kernel='linear', probability=True)
        self.clf.fit(tf_train, result_train['is_offensive'].tolist())
        pred = self.clf.predict(tf_test)
        result_test_arr = result_test['is_offensive'].tolist()
        # print(len(result_test_arr))
        # print(len(pred))
        correctPred = 0
        wrongPred   = 0
        class0 = 0
        class1 = 0
        class2 = 0
        for indx, val in enumerate(pred):
            if val == result_test_arr[indx]:
                correctPred += 1
            else:
                wrongPred += 1
                if str(val) == '0':
                    class0 = class0 +1
                elif str(val) == '1':
                    class1 = class1 +1
                else:
                    class2 = class2 +1
        # print('class0>>' + str(class0))
        # print('class1>>' + str(class1))
        # print('class2>>' + str(class2))
        # print('model accuracy:' + str((correctPred/(wrongPred+correctPred))*100) )
        modelName = 'textExtractionAndProfaneChecking/models/model/model.sav'
        pickle.dump(self.clf, open(modelName, 'wb'))
        vectorizerName = 'textExtractionAndProfaneChecking/models/model/vectorizer.pk'
        pickle.dump(self.vectorizer, open(vectorizerName, 'wb'))

    def predict(self, text):
        text_df = pd.DataFrame(columns=['text'])
        text_df.loc[-1] = [text]
        tf_ext = self.vectorizer.transform(text_df['text'])
        #tf_ext = self.bClient.encode(text_df['text'].tolist())
        pred  = self.clf.predict(tf_ext)
        pred_proba = self.clf.predict_proba(tf_ext)
        #print('--------------------------------------')
        #print(pred)
        #print(pred_proba)
        #print(self.clf.classes_)
        #print('--------------------------------------')

        highest_proba = max(pred_proba[0])
        if pred[0] == 0:
            return {"classification" : "Not Offensive" ,
                "probability" : highest_proba , 'text' : text }
        elif pred[0] == 1:
            return {"classification" : "Offensive" ,
                "probability" : highest_proba, 'text' : text }
