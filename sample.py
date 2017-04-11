# @Author: Karthick <ramya>
# @Date:   2017-04-06T11:40:41+02:00
# @Last modified by:   ramya
# @Last modified time: 2017-04-11T08:41:27+02:00



from __future__ import print_function
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, Dropout, Embedding, Flatten
from keras.layers import LSTM, Convolution1D, MaxPooling1D, Bidirectional, TimeDistributed, GRU, Input, merge, AveragePooling1D, SimpleRNN
from keras.layers.merge import concatenate
from keras.optimizers import RMSprop, Adam
from keras.utils.data_utils import get_file
from keras.layers.normalization import BatchNormalization
from keras.callbacks import Callback, ModelCheckpoint
from sklearn.decomposition import PCA
import numpy as np
import random
import sys
import csv
import os
import h5py
import argparse

parser = argparse.ArgumentParser()

## Joke data set and relevant information for reading the data
parser.add_argument("--model_file", type = str, default= "save/model.hdf5",
					help = "path of the  model weights file")

parser.add_argument("--data_file", type = str, default= "reduced_char_jokes.txt",
					help = "path of the data file")

parser.add_argument("--length", type = int, default = 5000,
					help = "required length of generated text")

parser.add_argument("--prime", type = str, default= "",
					help = "Seed text, you can warmup the text generation with initial seed")

parser.add_argument("--temperature", type = float, default = 0.5,
					help = "diversity of gnenerated text - temperature: 0 for conservtive output and 1 for exploratory output")


args = parser.parse_args()


maxlen = 200  # must match length which generated model
num_char_generated = args.length

text = open(args.data_file).read()

chars = sorted(list(set(text)))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

step = 1
sentences = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])

print('Vectorization...')
X = np.zeros((len(sentences), maxlen), dtype=np.int)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t] = char_indices[char]

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-6) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

print('Loading model...')
model = load_model('output/model.hdf5')
f2 = open('output/text_sample.txt', 'w')

start_index = random.randint(0, len(text) - maxlen - 1)

generated = ""
sentence = args.prime
generated += sentence
sys.stdout.write(generated)

for i in range(args.length):
    x = np.zeros((1, maxlen), dtype=np.int)
    for t, char in enumerate(sentence):
        x[0, t] = char_indices[char]

    preds = model.predict(x, verbose=0)[0][0]
    next_index = sample(preds, args.temperature)
    next_char = indices_char[next_index]

    generated += next_char
    sentence = sentence[1:] + next_char

    sys.stdout.write(next_char)
    sys.stdout.flush()
