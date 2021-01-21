import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import random
import tensorflow
from tensorflow.python.framework import ops
import json
import os
import pickle
os.environ['KMP_DUPLICATE_LIB_OK']='True'

stemmer = LancasterStemmer()

with open('./data/intents.json') as file:
    data = json.load(file)

training = []
output = []


def retrain_model():
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
        # Word tokenizing
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            if intent["tag"] not in labels:
                labels.append(intent["tag"])
            
    words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    # Creating bag of words in any pattern
    # I.e ["a", "little","zebra",...] => [0,0,0,...]

    out_empty = [0 for _ in range(len(labels))]

    for x,doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc] #Current pattern

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("./data/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output),f)



# Main function

try:
    with open("./data/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    retrain_model()


ops.reset_default_graph()
# Start with the length of input data
net = tflearn.input_data(shape=[None, len(training[0])]) # The input layers
net = tflearn.fully_connected(net, 8) # 8 neuron of hidden layers
net = tflearn.fully_connected(net, 8) # 8 neuron of hidden layers
net = tflearn.fully_connected(net, len(output[0]), activation="softmax") # 8 neuron of hidden layers (output layer) 
# Softmax is giving out probability of each neuron => Take the highest probability
net = tflearn.regression(net)

# DNN - type of neural network
model = tflearn.DNN(net)

model.fit(training, output, n_epoch = 1000, batch_size = 8, show_metric = True)
model.save("./data/model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)

def chat():
    print("Start talking with the bot")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        #Giving out probability
        results = model.predict([bag_of_words(inp, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.85:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg["responses"]
            print(random.choice(responses))
        else:
            print("Wdym?")
chat()