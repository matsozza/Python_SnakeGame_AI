# importing libraries
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import os
import copy

class NeuralNetwork:
    # Basic methods for ANN math
    def __init__(self, network_topology = [9,18,3], draw = False) -> None:
        # Initialize weights and biases randomly within a certain range
        self.network_topology = network_topology
        self.actv_fcns = [None, NeuralNetwork.relu, NeuralNetwork.softmax]
        self.draw = draw
      
        # Initialize layers, weights, and biases
        self.layers = [np.zeros(size) for size in network_topology]  # Empty neurons
        self.biases = [np.random.uniform(-1, 1, size) for size in network_topology[1:]]  # No biases for input layer
        self.weights = [np.random.uniform(-1,1,(network_topology[i], network_topology[i + 1]))
                        for i in range(len(network_topology) - 1)]  # Small random weights
                
        # Calculate nodes position for graph drawing (if applicable)
        if self.draw:
            matplotlib.use('TkAgg')  # Use the TkAgg backend
            self.init_plot()

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
        # Feed the first layer with inputs - no activation fcn, no biases
        self.layers[0] = inputs
        
        # Do the forward propagation with weights, biases and actv. function
        num_layers = len(self.network_topology)
        for layer_num in range(1,num_layers):
            self.layers[layer_num] = self.actv_fcns[layer_num]((self.layers[layer_num-1] @ self.weights[layer_num-1]) + self.biases[layer_num-1])

        # Draw updated version of ANN + activations
        if self.draw:
            self.plot()

        # Return idx. of biggest value in the output layer (one-hot)
        return np.argmax(self.layers[-1], axis = 0)   

    def set_weights_biases(self,weights,biases):
        self.weights = copy.deepcopy(weights)
        self.biases = copy.deepcopy(biases)

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

    # Graphic methods for AN plotting (tks, ChatGPT! :D)
    def init_plot(self):
        """
        Calculate the (x, y) positions for each node in the layers.
        """
        
        # Define nodes positions
        x_spacing = 1.5
        y_spacing = 1.5
        node_positions = []
        for i, num_nodes in enumerate(self.network_topology):
            x = i * x_spacing
            y_positions = np.linspace(
                -(num_nodes - 1) * y_spacing / 2,
                (num_nodes - 1) * y_spacing / 2,
                num_nodes
            )
            layer_positions = [(x, y) for y in y_positions]
            node_positions.append(layer_positions)
            
        # Create instance variables for standalone fig. management
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        self.node_positions = node_positions
        
        manager = plt.get_current_fig_manager()
        manager.window.wm_geometry(f"+{750}+{0}")
        self.fig.canvas.manager.set_window_title("ANN Live Performance")
        
        # Enable interactive mode
        plt.ion()
        plt.show(block=False)
        
    def plot(self):
        """Plot the neural network with activations."""
        # Clear the axes to avoid overwriting previous drawings
        self.ax.clear()
        self.ax.axis("off")

        # Draw nodes (neurons)
        for i, layer in enumerate(self.node_positions):
            activation = self.layers[i]
            max_activation = np.max(activation)
            min_activation = np.min(activation)

            for j, (x, y) in enumerate(layer):
                # Color neurons based on activation values
                color = plt.cm.RdBu((activation[j] - min_activation) / np.maximum(max_activation - min_activation, 1e-6))
                self.ax.scatter(x, y, s=2000, color=color, zorder=3, edgecolors='black')

                # Calculate brightness of the color (using luminance formula)
                luminance = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
                # Choose annotation color based on luminance
                annotation_color = 'black' if luminance > 0.5 else 'white'

                # Add activation value inside the neuron
                self.ax.text(x, y, f"{activation[j]:.2f}", ha="center", va="center", fontsize=10, color=annotation_color, zorder=4)

        # Draw connections (edges between layers)
        for i in range(len(self.network_topology) - 1):
            for start_pos, start_activation, start_weights in zip(self.node_positions[i], self.layers[i], self.weights[i]):
                for end_pos, end_activation, weight in zip(self.node_positions[i + 1], self.layers[i + 1], start_weights.T):
                    # Calculate the connection effect based on activation * weight
                    weight_regularized = 2 * (weight - np.min(self.weights[i])) / (np.max(self.weights[i]) - np.min(self.weights[i])) - 1
                    
                    if np.max(self.layers[i]) != np.min(self.layers[i]):
                        activation_regularized = np.abs(2 * (start_activation - np.min(self.layers[i])) / (np.max(self.layers[i]) - np.min(self.layers[i])) - 1)
                    else:
                        activation_regularized = 1

                    # Normalize the value for color and thickness
                    connection_color = plt.cm.RdBu(weight_regularized)  # Normalize to [0, 1] range
                    line_thickness = 8*activation_regularized*weight_regularized   # Adjust thickness based on combined magnitude

                    self.ax.plot(
                        [start_pos[0], end_pos[0]],
                        [start_pos[1], end_pos[1]],
                        color=connection_color,
                        linewidth=line_thickness,
                        alpha=0.7,
                        zorder=1
                    )

        # Add annotations for layers
        for i, (layer, num_nodes) in enumerate(zip(self.node_positions, self.network_topology)):
            self.ax.text(
                layer[0][0], max(y for _, y in layer) + 1.5,
                f"Layer {i+1} ({num_nodes} nodes)",
                ha="center",
                fontsize=10,
                color="black"
            )

        # Redraw the figure
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

