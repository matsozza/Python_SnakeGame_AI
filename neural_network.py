import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.datasets import mnist
import tensorflow as tf

# Snake Game - Training Model
# 8 inputs: Current snake position in table (2) + current food position in table (2) + Current direction (4)
# 4 outputs: new direction
def snake_model():
    model = Sequential()
    model.add(Dense(units=16, activation='relu', input_shape=(8,)))
    model.add(Dense(units=4, activation='softmax')) # UP DOWN LEFT RIGHT
    #model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def gen_mutant(parent_model, mutation_rate, mutation_size):
    layers = parent_model.layers
    for idx, layer in enumerate(layers):
        l_weights = layer.get_weights()[0] # weights in the given layer (2D)
        l_biases = layer.get_weights()[1] # biases in the given layer (1D)
        print("Total weights in layer: ", str(np.shape(l_weights)[0] * np.shape(l_weights)[1]))

        # Loop into each weight in the current layer and apply mutation
        for w_row in np.arange(np.shape(l_weights)[0]):
            for w_col in np.arange(np.shape(l_weights)[1]):
                if np.random.binomial(1, mutation_rate) == 1: # Mutate
                    w = l_weights[w_row][w_col]
                    print("W_before -> ", str(w))

                    # Generate a mutation and bound it within +-1
                    w = np.random.normal(w, mutation_size)
                    if w > 1:
                        w = 1
                    elif w < -1:
                        w = -1
                    print("W_after -> ", str(w))