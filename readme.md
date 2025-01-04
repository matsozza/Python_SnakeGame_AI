# Snake Game in Python trained by AI Genetic Algorithm

This project consists in an implementation of the classic Nokia Snake Game in Python.

The user can choose either to play manually the game in a NxN table (adjustable) or can set many instances of the game to be played by an Artificial Neural Network (ANN) while also training it through many generations.

---

### Miniclip:

[![Snake AI Miniclip](https://img.youtube.com/vi/8lji1RB53hQ/0.jpg)](https://youtu.be/watch?v=8lji1RB53hQ)

---
### Summary:

The game is implemented based on some main files:
- **MainParl.ipynb**: Python Notebook where the user can tune some high level parameters and choose some things such as:
  - Whether to play manually or using the AI inputs.
  - Whether to show visuals or not.
  - Tune parameters for AI training
  - etc...
- **SnakeGame.py**: Game logics ("backend") implementation. Used for training the ANN, decoupled from visuals / graphics.
- **SnakeBoard.py**: Visuals class, used to show the game board for manual playing or for tracking the training progress visually.
- **NeuralNetwork.py**: Manual implementation of a generic ANN and some of its methods (mutate, calculate, initialize, get/set weights and biases, etc...)

This repo can be updated at anytime, so maybe this readme becomes somewhat obsolete - I created this project just for fun. Have fun too!