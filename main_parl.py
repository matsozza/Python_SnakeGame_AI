import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

import tensorflow
import keras

from SnakeGame import SnakeGame
import neural_network
import numpy as np
from multiprocessing import Pool

def main():
    if __name__ == '__main__':
        print("----- START -----")

        num_of_games = 15
        num_of_gens = 100000

        # Start args for each model instance for each game
        args_w = []
        for idx in np.arange(num_of_games):
            args_w.append((SnakeGame(idx), neural_network.nn_model()))
        
        idx_gen=0
        while idx_gen < num_of_gens:

            # Run a pool with a number of games (generation)
            results = []
            with Pool(num_of_games) as p:
                idx_gen=idx_gen+1
                
                print("----- GEN START ", idx_gen, " -----")
                # Use the pool's apply_async method to asynchronously execute tasks
                async_results = [p.apply_async(game_instance, args) for args in args_w]

                # Use the pool's wait method to wait for all processes to finish
                p.close()
                p.join()

                # Get the results from the asynchronous tasks
                results = [async_result.get() for async_result in async_results] # Array with scores
                print("----- GEN END ", idx_gen, " -----")

            # Get best score in prev. generation
            max_res = max(enumerate(results),key=lambda x: x[1])[0]
            print(" ----- BEST SCORE: ", np.max(results), " -----")

            # Create mutate models based on best of prev. gen.
            args_w[0] =  (args_w[0][0], keras.models.clone_model(args_w[max_res][1]) ) # Put best model in 0
            for idx in np.arange(num_of_games)[1:]:
                args_w[idx] = (args_w[idx][0], keras.models.clone_model(args_w[0][1]) ) # Clone best model in 1...end
                neural_network.nn_mutate(args_w[idx][1], 0.1, 0.5) # Mutate best model in 1...end

        print("----- END -----") 

def game_instance(game_obj, model_obj):
    next_move = 'IDLE'
    for i in range(10000): 
        [game_over, state, score] = game_obj.step_game(next_move)
        print("State->", state, " Index -> ", i)
        next_move = neural_network.nn_get_output(model_obj, state)
        
        if next_move == 0: next_move = "UP"
        if next_move == 1: next_move = "DOWN"
        if next_move == 2: next_move = "LEFT"
        if next_move == 3: next_move = "RIGHT"

        print(next_move)

        if game_over == 1:
            return score
        
        if i> 250*(score+1):
            print("TIMEOUT")
            return 0
        

    return score   
# ********** Executable code **********
main()