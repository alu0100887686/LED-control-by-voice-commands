from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import batch # some methods to procces audio batchs

INPUT_DIM = 8
INPUT_LAYER_SIZE = 8
HIDDEN_LAYER_SIZE = 12
OUTPUT_LAYER_SIZE = 8
INPUT_LAYER_ACTIVATION = 'relu'
HIDDEN_LAYER_ACTIVATION = 'relu'
OUTPUT_LAYER_ACTIVATION = 'sigmoid'

# fix random seed for reproducibility
np.random.seed(7)  

def build_from_scratch():
    # create model
    model = Sequential()
    model.add(Dense(INPUT_LAYER_SIZE, input_dim = INPUT_DIM, activation = INPUT_LAYER_ACTIVATION))
    model.add(Dense(HIDDEN_LAYER_SIZE, activation = HIDDEN_LAYER_ACTIVATION))
    model.add(Dense(OUTPUT_LAYER_SIZE, activation = OUTPUT_LAYER_ACTIVATION))
    return model

def evaluate(model, validation_set_path = "../../data/validation_set", dictionary_path = "../../data/dictionary.csv"):
    X, Y = batch(training_set_path, dictionary_path)
    # evaluate the model
    scores = model.evaluate(x, y, batch_size=len(x))
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    
def training(training_set_path = "../../data/training_set", dictionary_path = "../../data/dictionary.csv"):
    model = build_from_scratch()
    x, y = batch(training_set_path, dictionary_path)
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(x, y, epochs=150, batch_size=len(x))
    evaluate(model)
    return model

def export_model(model, json_model_path = "../../data/model/model.json", hdf5_weights_path = "../../data/model/model.h5"):
    # serialize model to JSON
    model_json = model.to_json()
    with open(json_model_path, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(hdf5_weights_path)
    print("Saved model to disk")

def import_model(model, json_model_path = "../../data/model/model.json", hdf5_weights_path = "../../data/model/model.h5"):
    # load json and create model
    json_file = open(json_model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("../../data/model/model.h5")
    return loaded_model
    print("Loaded model from disk")