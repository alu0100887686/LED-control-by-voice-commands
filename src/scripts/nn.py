#!/usr/bin/python
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import LSTM
from keras.layers import Dropout
from keras import optimizers
import numpy as np
import batch # some methods to procces audio batchs
import time
import h5py
import sys, os

units_first_layer = 1024
units_second_layer = 1024
units_third_layer = 1024
classes = 2
epochs = 25
path = os.path.dirname(__file__)
training_set_path = path + '/../../data/training_set'
validation_set_path = path + '/../../data/validation_set'
dictionary_path = path + '/../../data/dictionary.csv'
json_path = path + '/../../data/model/model.json'
h5_path = path + '/../../data/model/weights.h5'

def generate_model(training_set_path = training_set_path, validation_set_path = training_set_path,
 dictionary_path = dictionary_path, json_path = json_path, h5_path = h5_path):
    # fix random seed for reproducibility
    np.random.seed(int(time.time()))
    # get training batch
    x_t, y_t = batch.batch(training_set_path, dictionary_path)
    # get validation batch
    x_v, y_v = batch.batch(validation_set_path, dictionary_path)
    print("- Training and validation sets imported.")
    # create model
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, stateful=False, batch_input_shape = (None, x_t.shape[1], x_t.shape[2])))
    model.add(LSTM(64, return_sequences=True, stateful=False))
    model.add(LSTM(64, stateful=False))
    # add dropout to control for overfitting
    model.add(Dropout(.25))
    # squash output onto number of classes in probability space
    model.add(Dense(classes, activation='softmax'))
    # compile the model
    model.compile(loss='categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])
    # Fit the model
    model.fit(x_t, y_t, epochs = epochs, validation_data=(x_v, y_v))
    # export model
    # serialize model to JSON
    model_json = model.to_json()
    with open(json_path, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(h5_path)
    print("- Model exported to disk.")
    return model

def import_model(json_path = json_path, h5_path = h5_path):
    # load json and create model
    json_file = open(json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(h5_path)
    print("Model loaded from disk.")
    return loaded_model

def predict(model, x_path): # should be specified a model an a audio instance
    x = batch.features(x_path)
    return np.argmax(model.predict(np.array(x)))

generate_model()
