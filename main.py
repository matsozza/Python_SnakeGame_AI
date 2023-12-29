import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import snake
import neural_network
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
from multiprocessing import Pool

def main():
    if __name__ == '__main__':
        print("----- START -----")

        num_of_games = 2
        num_of_gens = 10

        # Start args for each model instance for each game
        args_w = []
        for idx in np.arange(num_of_games):
            args_w.append((neural_network.nn_model(),idx))
        
        i=0
        while i < num_of_gens:

            # Run a pool with a number of games (generation)
            results = []
            with Pool(num_of_games) as p:
                i=i+1
                
                print("----- GEN START -----")
                # Use the pool's apply_async method to asynchronously execute tasks
                async_results = [p.apply_async(snake.run_game, args) for args in args_w]

                # Use the pool's wait method to wait for all processes to finish
                p.close()
                p.join()

                # Get the results from the asynchronous tasks
                results = [async_result.get() for async_result in async_results] # Array with scores
                print("----- GEN END -----")

            # Get best score in prev. generation
            max_res = max(enumerate(results),key=lambda x: x[1])[0]
            print(" ----- BEST SCORE: ", np.max(results), " -----")

            # Create mutate models based on best of prev. gen.
            args_w[0] = (keras.models.clone_model(args_w[max_res][0]), 0)
            for idx in np.arange(num_of_games)[1:]:
                args_w[idx] = (keras.models.clone_model(args_w[0][0]), idx)
                neural_network.nn_mutate(args_w[idx][0], 0.15, 0.15)

        print("----- END -----") 

# ********** Executable code **********
main()