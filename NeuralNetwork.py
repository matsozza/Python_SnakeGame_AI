import numpy as np
import math
import copy

class NeuralNetwork:
    size_input_layer = 5
    size_hidden_layer = 8
    size_output_layer = 3

    def __init__(self) -> None:
        self.weights = []
        self.biases = []

        self.weights.append(np.zeros(  [NeuralNetwork.size_input_layer, NeuralNetwork.size_hidden_layer  ]))
        self.biases.append(np.zeros(  [NeuralNetwork.size_hidden_layer  ]))

        self.weights.append(np.zeros(  [NeuralNetwork.size_hidden_layer, NeuralNetwork.size_output_layer  ]))
        self.biases.append(np.zeros(  [NeuralNetwork.size_output_layer  ]))

        self.mutate(1,0.05) # Random mutation in 100% of the weights for start-up

    def mutate(self,rate_w,size_w, rate_b=0, size_b=0):
        # Sweep each layer of the architecture
        for idx, layer in enumerate(self.weights):
            l_weights = self.weights[idx] # weights in the given layer (2D)
            l_biases = self.biases[idx] # biases in the given layer (1D)
            #print("Total weights in layer: ", str(np.shape(l_weights)[0] * np.shape(l_weights)[1]))

            # Loop into each weight in the current layer and apply mutation
            for w_row in np.arange(np.shape(l_weights)[0]):
                for w_col in np.arange(np.shape(l_weights)[1]):
                    if np.random.binomial(1, rate_w) == 1: # Mutate
                        w = l_weights[w_row][w_col]
                        w_old = w
                        
                        # Generate a mutation and bound it within +-1
                        w = np.random.normal(w, size_w)
                        if w > 1:
                            pass #w = 1
                        elif w < -1:
                            pass #w = -1
                        #print("W_before -> ", str(w_old), " w_aft ->", str(w))
                        l_weights[w_row][w_col] = w
            
            # Loop into each bias in the current layer and apply mutation
            for b_row in np.arange(np.shape(l_biases)[0]):
                if np.random.binomial(1, rate_b) == 1: # Mutate
                    b = l_biases[b_row]
                    b_old = b
                    
                    # Generate a mutation and bound it within +-1
                    b = np.random.normal(b, size_b)
                    if b > 1:
                        pass #b = 1
                    elif b < -1:
                        pass #b = -1
                    #print("B_before -> ", str(b_old), " b_aft ->", str(b))
                    l_biases[b_row] = b
            
            self.weights[idx] = l_weights
            self.biases[idx] = l_biases

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()
    
    def relu(x):
        for i,v in enumerate(x):
            if v<0: 
                x[i]=0
        return x
    
    def tanh(x):
        for i,v in enumerate(x):
            x[i]=math.tanh(v)
        return x  

    def calculate(self, inputs):
        #print("Input:", input)
        l0 = inputs @ self.weights[0]
        l0 = l0 + self.biases[0]
        l0 = NeuralNetwork.softmax(l0)
        #print("l0:", l0)

        l1 = l0 @ self.weights[1]
        l1 = l1 + self.biases[1]
        l1 = NeuralNetwork.relu(l1)
        #print("l1:", l1)
        return np.argmax(l1, axis = 0)
    
    def clone(self,neural_network):
        self.weights = neural_network.weights
        self.biases = neural_network.biases

    def __copy__(self):
        new_obj = self.__class__()
        for k,v in vars(self).items():
            try:
                setattr(new_obj, k, copy.deepcopy(v))
            except:
                pass   # non-pickelable stuff wasn't needed

            return new_obj

    def copy(self):
        return self.__copy__()