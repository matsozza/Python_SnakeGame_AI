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

        num_of_games = 8
        num_of_gens = 10

        # Start args for each model instance for each game
        args_w = []
        for idx in np.arange(num_of_games):
            args_w.append((SnakeGame(idx), neural_network.nn_model()))
        
        i=0
        while i < num_of_gens:

            # Run a pool with a number of games (generation)
            results = []
            with Pool(num_of_games) as p:
                i=i+1
                
                print("----- GEN START -----")
                # Use the pool's apply_async method to asynchronously execute tasks
                async_results = [p.apply_async(game_instance, args) for args in args_w]

                # Use the pool's wait method to wait for all processes to finish
                #p.close()
                #p.join()

                # Get the results from the asynchronous tasks
                results = [async_result.get() for async_result in async_results] # Array with scores
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