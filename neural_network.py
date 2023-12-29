import numpy as np
from keras.models import Sequential
from keras.layers import Dense
#import tensorflow as tf
#import sklearn as sk

# Snake Game - Training Model
# 8 inputs: Current snake position in table (2) + current food position in table (2) + Current direction (4)
# 4 outputs: new direction
def nn_model():
    model = Sequential()
    model.add(Dense(units=16, activation='relu', input_shape=(8,)))
    model.add(Dense(units=32, activation='relu', input_shape=(8,)))
    model.add(Dense(units=4, activation='relu')) # UP DOWN LEFT RIGHT
    nn_mutate(model, 0.1, 0.5)
    return model

def nn_mutate(nn_model, mutation_rate, mutation_size):
    layers = nn_model.layers
    # Sweep each layer of the architecture
    for idx, layer in enumerate(layers):
        l_weights = layer.get_weights()[0] # weights in the given layer (2D)
        l_biases = layer.get_weights()[1] # biases in the given layer (1D)
        #print("Total weights in layer: ", str(np.shape(l_weights)[0] * np.shape(l_weights)[1]))

        # Loop into each weight in the current layer and apply mutation
        for w_row in np.arange(np.shape(l_weights)[0]):
            for w_col in np.arange(np.shape(l_weights)[1]):
                if np.random.binomial(1, mutation_rate) == 1: # Mutate
                    w = l_weights[w_row][w_col]
                    #w_old = w
                    
                    # Generate a mutation and bound it within +-1
                    w = np.random.normal(w, mutation_size)
                    if w > 1:
                        w = 1
                    elif w < -1:
                        w = -1
                    #print("W_before -> ", str(w_old), " w_aft ->", str(w))

                    l_weights[w_row][w_col] = w
        layer.set_weights([l_weights, l_biases])

def nn_get_output(model, inputs):
    inputs = np.array(inputs).reshape([1, -1])
    output = model.predict(inputs, verbose = 0)
    #print("nn_get_output -> ", output, " --- ", np.argmax(output, axis = 1))
    return np.argmax(output, axis = 1)