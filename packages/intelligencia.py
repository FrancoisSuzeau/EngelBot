import nltk
# if punkt is not uodated 
# nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn as tfl

# disable tensorflow message telling  that it can and will use CPU optimization 
import os; 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tsf
import random as rd
import json as js
import pickle as pi

import shutil

class Intelligencia():
    def __init__(self):
        self.words = []
        self.labels = []
        self.training = []
        self.output = []
        self._tolerance = 0
        self._epoch = 0

        self.load_config()
        self.load_data()
        self.preprocess_data()
        self.train_model()

    def clean_cache(self):
        shutil.rmtree('materials/cache')
        os.mkdir(os.path.join('materials/', 'cache'))

    def load_data(self):
        with open("materials/data/intents.json") as file:
            self.data = js.load(file)

    def load_config(self):
        with open("materials/data/config.json") as file:
            config = js.load(file)['ML']
            self.epoch = config['epoch']
            self.tolerance = config['tolerance']

    def write_config(self):
        with open("materials/data/config.json", "r") as file:
            config = js.load(file)
        config['ML'] = {
            "epoch":self.epoch,
            "tolerance":self.tolerance
        }
        json_object = js.dumps(config, indent=2)
        with open("materials/data/config.json", "w") as outfile:
            outfile.write(json_object)
        self.load_config()

    @property
    def tolerance(self):
        return self._tolerance
    @tolerance.setter
    def tolerance(self, value):
        self._tolerance = value

    @property
    def epoch(self):
        return self._epoch
    @epoch.setter
    def epoch(self, value):
        self._epoch = value
    
# ======================================================================================== Preprocessing data ==============================================================================
    def preprocess_data(self):
        docs_x = []
        docs_y = []
        # we don't want to run the preprocessing step every time we make a prediction
        try:
            with open("materials/cache/data.pickle", "rb") as f:
                self.words, self.labels, self.training, self.output = pi.load(f)
        except:
            
            for intent in self.data["intents"]:
                print("Reading : " + intent['tag'])
                
                for pattern in intent["patterns"]:
                #if we have :
                # - "how are you ?" we keep "how are you" 
                # - "whats up" we keep what up
                # We want the root of the word : we are training our bot we doesn't care about the word but the main meaning -> make it more accurate
                    wrds = nltk.word_tokenize(pattern)
                    self.words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent['tag'])

                    if intent['tag'] not in self.labels:
                        self.labels.append(intent['tag']) 

            # don't know
            self.words = [stemmer.stem(w.lower()) for w in self.words if w not in "?"]
            # set will remove duplicates
            self.words = sorted(list(set(self.words)))
            self.labels = sorted(self.labels)

            # for now we only have strings and neural network understand numbers so we create a bag of words representing all the words in any given patterns to train our model
            # [0, 0, 0, 0, 1, 0, 1, 1, 1, 0] -> represent if a words exist or does not exist (could be value > to 1 and it says how many times the words exist)
            out_empty = [0 for _ in range(len(self.labels))]
            # the same way we use [0, 0, 1, ....] corresponding of labels
            print("Making all bags of word")
            i = 0
            for x, doc in enumerate(docs_x):
                bag = []
                wrds = [stemmer.stem(w) for w in doc]
                for w in self.words:
                    if w in wrds:
                        bag.append(1)
                    else:
                        bag.append(0)

                output_row = out_empty[:]
                output_row[self.labels.index(docs_y[x])] = 1

                self.training.append(bag)
                self.output.append(output_row)

            self.training = np.array(self.training)
            self.output = np.array(self.output)

            print("Writting bytes into file")
            with open("materials/cache/data.pickle", "wb") as f:
                pi.dump((self.words, self.labels, self.training, self.output), f)

# ======================================================================================== training learning model ============================================================================
    def train_model(self):

        tsf.compat.v1.reset_default_graph()

        net = tfl.input_data(shape=[None, len(self.training[0])])
        net = tfl.fully_connected(net, 8)
        net = tfl.fully_connected(net, 8)
        # softmax will give probability to each neurons output 
        net = tfl.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tfl.regression(net)

        self.model = tfl.DNN(net)

        try:
            self.model.load("materials/cache/model.tflearn")
        except:
            self.model = tfl.DNN(net)
            self.model.fit(self.training, self.output, n_epoch=self.epoch, batch_size=8, show_metric=True)
            self.model.save("materials/cache/model.tflearn")

# ======================================================================================== prediction ========================================================================================
    def bag_of_words(self, s):
        bag = [0 for _ in range(len(self.words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1

        return np.array(bag)

    def chat(self, inp):
        # have a bbunch of probabilty of each output neuron and not a string
        results = self.model.predict([self.bag_of_words(inp)])[0]
        #we want the one with higher probability
        result_index = np.argmax(results)
        #this give us the better tag correspondingg of our input
        tag = self.labels[result_index]

        if results[result_index] >= self.tolerance:
            for tg in self.data['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            return rd.choice(responses)
        else:
            return "(Very softly) Ok"


if __name__ == "__main__":
    intel = Intelligencia()
    # print(intel.training)