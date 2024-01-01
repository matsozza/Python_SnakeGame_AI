import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from SnakeGame import SnakeGame
import neural_network
import numpy as np
import keras
from multiprocessing import Pool

def main():
    if __name__ == '__main__':
        print("----- START -----")

        num_of_games = 10
        num_of_gens = 10000

        # Start args for each model instance for each game
        args_w = []
        for idx in np.arange(num_of_games):
            args_w.append((SnakeGame(0), neural_network.nn_model()))
        
        idx_gen=0
        for idx_gen in np.arange(num_of_gens):
            # Run a pool with a number of games (generation)
            results = np.zeros(num_of_games)
            for idx_game in np.arange(num_of_games):                
                print("----- GEN START -----")
                # Use the pool's apply_async method to asynchronously execute tasks
                score = game_instance(args_w[idx_game][0],args_w[idx_game][1])

                # Get the results from the asynchronous tasks
                results[idx_game] = score
                print("----- GEN END -----")

            # Get best score in prev. generation
            max_res = max(enumerate(results),key=lambda x: x[1])[0]
            print(" ----- BEST SCORE: ", np.max(results), " -----")

            # Create mutate models based on best of prev. gen.
            args_w[0] =  (args_w[0][0], keras.models.clone_model(args_w[max_res][1]) ) # Put best model in 0
            for idx in np.arange(num_of_games)[1:]:
                args_w[idx] = (args_w[idx][0], keras.models.clone_model(args_w[0][1]) ) # Clone best model in 1...end
                neural_network.nn_mutate(args_w[idx][1], 0.15, 0.15) # Mutate best model in 1...end
            
        print("----- END -----") 

def game_instance(game_obj, model_obj):
    next_move = 'IDLE'
    for i in np.arange(1000): 
        [game_over, state, score] = game_obj.step_game(next_move)
        next_move = neural_network.nn_get_output(model_obj, state)
        
        if next_move == 0: next_move = "UP"
        if next_move == 1: next_move = "DOWN"
        if next_move == 2: next_move = "LEFT"
        if next_move == 3: next_move = "RIGHT"


        if game_over == 1:
            return score
        
# ********** Executable code **********
main()