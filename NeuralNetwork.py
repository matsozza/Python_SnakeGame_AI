# importing libraries
import numpy as np
import copy

class NeuralNetwork:
    def __init__(self) -> None:
        # Initialize weights and biases randomly within a certain range
        self.network_topology = [6,6,3]
        self.weights = []
        self.biases = []
        
        num_layers = len(self.network_topology)
        for layer_num in range(num_layers-1):
                w= np.random.uniform(-0.1, 0.1,
                    [self.network_topology[layer_num], self.network_topology[layer_num+1]])
                b= np.random.uniform(-0.1, 0.1, 
                    self.network_topology[layer_num+1])
                self.weights.append(w)
                self.biases.append(b)      

    def mutate(self, rate_w, size_w, rate_b, size_b):
        # Loop through each layer in the neural network
        for idx in range(len(self.weights)):
            # Create vector of mutation for weights
            selected_weights = np.random.binomial(1, rate_w, size=self.weights[idx].shape).astype(bool)
            mutation_offset_weights = np.random.normal(0, size_w, size=self.weights[idx].shape)
            
            # Apply mutation and clip values between -1 +1
            self.weights[idx][selected_weights] += mutation_offset_weights[selected_weights]
            self.weights[idx] = np.clip(self.weights[idx], -1, 1)  

            # Create vector of mutation for biases
            selected_biases = np.random.binomial(1, rate_b, size=self.biases[idx].shape).astype(bool)
            mutation_offset_biases = np.random.normal(0, size_b, size=self.biases[idx].shape)
            
            # Apply mutation and clip values between -1 +1
            self.biases[idx][selected_biases] += mutation_offset_biases[selected_biases]
            self.biases[idx] = np.clip(self.biases[idx], -1, 1)  

    def softmax(x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)
    
    def relu(x):
        return np.maximum(0, x)

    def tanh(x):
        return np.tanh(x)

    def calculate(self, inputs):
        l0 = NeuralNetwork.relu((inputs @ self.weights[0]) + self.biases[0])
        l1 =  NeuralNetwork.softmax((l0 @ self.weights[1])  + self.biases[1])
        #print("Input:", input)
        #print("l0:", l0)
        #print("l1:", l1)
        return np.argmax(l1, axis = 0)

    def set_weights_biases(self,weights,biases):
        self.weights = weights
        self.biases = biases

    def __copy__(self):
        new_obj = self.__class__()
        for k,v in vars(self).items():
            try:
                setattr(new_obj, k, copy.deepcopy(v))
            except:
                pass
        return new_obj

    def copy(self):
        return self.__copy__()