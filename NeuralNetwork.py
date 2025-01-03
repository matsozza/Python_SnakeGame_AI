# importing libraries
import numpy as np
import os
import copy

class NeuralNetwork:
    def __init__(self) -> None:
        # Initialize weights and biases randomly within a certain range
        self.network_topology = [8,4,3]
        self.network_fcn = [None, NeuralNetwork.softmax, NeuralNetwork.relu]
        self.weights = []
        self.biases = []
        self.layers = []
        
        num_layers = len(self.network_topology)
        
        # Initialize neurons and biases
        self.layers.append(np.zeros(self.network_topology[0]))
        for layer_num in range(1,num_layers):
            b= np.random.uniform(-1, 1, self.network_topology[layer_num])
            self.biases.append(b) 
            self.layers.append(b) # Layer init. act is the bias
        
        # Initialize weights
        for layer_num in range(num_layers-1):
                w= np.random.uniform(-1, 1, [self.network_topology[layer_num], self.network_topology[layer_num+1]])
                self.weights.append(w)
     

    def mutate(self, rate_w, size_w, rate_b, size_b):
        # Loop through each layer in the neural network
        for idx in range(len(self.weights)):
            # Create vector of mutation for weights
            selected_weights = np.random.binomial(1, rate_w, size=self.weights[idx].shape).astype(bool)
            mutation_offset_weights = np.random.normal(0, size_w, size=self.weights[idx].shape)
            
            # Apply mutation and clip values between -1 +1
            self.weights[idx][selected_weights] += mutation_offset_weights[selected_weights]
            #self.weights[idx] = np.clip(self.weights[idx], -1, 1)  

            # Create vector of mutation for biases
            selected_biases = np.random.binomial(1, rate_b, size=self.biases[idx].shape).astype(bool)
            mutation_offset_biases = np.random.normal(0, size_b, size=self.biases[idx].shape)
            
            # Apply mutation and clip values between -1 +1
            self.biases[idx][selected_biases] += mutation_offset_biases[selected_biases]
            #self.biases[idx] = np.clip(self.biases[idx], -1, 1)  

    def softmax(x):
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)
    
    def relu(x):
        return np.maximum(0, x)

    def tanh(x):
        return np.tanh(x)

    def calculate(self, inputs):
        # Feed the first layer with inputs - no activation fcn, no biases
        self.layers[0] = inputs
        
        # Do the forward propagation with weights, biases and actv. function
        num_layers = len(self.network_topology)
        for layer_num in range(1,num_layers):
            self.layers[layer_num] = self.network_fcn[layer_num]((self.layers[layer_num-1] @ self.weights[layer_num-1]) + self.biases[layer_num-1])

        # Return idx. of biggest value in the output layer (one-hot)
        return np.argmax(self.layers[-1], axis = 0)

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
    
    def save_weights_biases(self, file_path):
        """Save the weights and biases to a .npz file."""
        dir = os.path.dirname(file_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        np.savez(file_path,
                 weights=np.array(self.weights, dtype=object), 
                 biases=np.array(self.biases, dtype=object))

    def load_weights_biases(self, file_path):
        """Load the weights and biases from a .npz file."""
        data = np.load(file_path, allow_pickle=True)
        self.weights = list(data['weights'])
        self.biases = list(data['biases'])
