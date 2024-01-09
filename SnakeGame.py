# importing libraries
import pygame
import time
import random
import numpy as np
import os

class SnakeGame:

#region ----- Class variables -----
#endregion

#region ----- Methods -----

    def __init__(self, snake_board):
        print("SnakeGame instance created.")
        self.start_game = 1
        self.snake_board = snake_board

    def init_game(self):
        # defining snake initial position
        self.pos_snake = [2*self.snake_board.WRES, 2*self.snake_board.WRES]

        # defining first blocks of snake body
        self.body_snake = [[2*self.snake_board.WRES, 2*self.snake_board.WRES], [1*self.snake_board.WRES, 2*self.snake_board.WRES]]
        
        # fruit position
        self.pos_food = [random.randrange(1, (self.snake_board.G_WIDTH//self.snake_board.WRES)) * self.snake_board.WRES, 
                        random.randrange(1, (self.snake_board.G_HEIGHT//self.snake_board.WRES)) * self.snake_board.WRES]

        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.score = 0 # initial score
        self.game_over = False

    def step_game(self, req_dir = "IDLE"):
        # Auto-start game if needed
        if self.start_game == 1:
            self.init_game()
            self.start_game=0

        # Run game and update state / score
        self._update_game_state(req_dir)
        #self._show_updated_score()

        # Check for game-over condition
        self.game_over = self._check_gameover()

        # Frame Per Second / Refresh Rate
        #self.fps.tick(self.snake_board.G_SPD)

        # Get game state
        state = self._get_game_state()
        return [self.game_over, state, self.score] # Game-over + score
    
    def _get_game_state(self):
        food_up = 1 if self.pos_snake[1] > self.pos_food[1] else 0
        food_dw = 1 if self.pos_snake[1] < self.pos_food[1] else 0
        food_left = 1 if self.pos_snake[0] > self.pos_food[0] else 0
        food_right = 1 if self.pos_snake[0] < self.pos_food[0] else 0

        dir_up = 1 if self.direction == 'UP' else 0
        dir_down = 1 if self.direction == 'DOWN' else 0
        dir_left = 1 if self.direction == 'LEFT' else 0
        dir_right = 1 if self.direction == 'RIGHT' else 0

        wall_up = 1 if self.pos_snake[1] == 0 else 0
        wall_down = 1 if self.pos_snake[1] == (self.snake_board.G_HEIGHT -  self.snake_board.WRES) else 0
        wall_left = 1 if self.pos_snake[0] == 0 else 0
        wall_right = 1 if self.pos_snake[0] == (self.snake_board.G_WIDTH -  self.snake_board.WRES) else 0   
        
        return [food_up, food_dw, food_left, food_right,
                dir_up, dir_down, dir_left, dir_right,
                wall_up, wall_down, wall_left, wall_right]

    def get_key(self):
        # If game not started, do not capture key
        if self.start_game == 1:
            return

        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 'UP'
                if event.key == pygame.K_DOWN:
                    return 'DOWN'
                if event.key == pygame.K_LEFT:
                    return 'LEFT'
                if event.key == pygame.K_RIGHT:
                    return 'RIGHT'
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    quit()
        return 'IDLE'

    def _update_game_state(self, req_dir):
        # Validate new requested direction
        if req_dir == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if req_dir == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if req_dir == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if req_dir == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'
        
        # Calculate new snake position
        if self.direction == 'UP':
            self.pos_snake[1] -= self.snake_board.WRES
        if self.direction == 'DOWN':
            self.pos_snake[1] += self.snake_board.WRES
        if self.direction == 'LEFT':
            self.pos_snake[0] -= self.snake_board.WRES
        if self.direction == 'RIGHT':
            self.pos_snake[0] += self.snake_board.WRES

        # Check if snake shall eat the food
        self.body_snake.insert(0, list(self.pos_snake))
        if self.pos_snake[0] == self.pos_food[0] and self.pos_snake[1] == self.pos_food[1]:
            self.score += 1 # grow snake
            self.pos_food = [random.randrange(1, (self.snake_board.G_WIDTH//self.snake_board.WRES)) * self.snake_board.WRES,
                                random.randrange(1, (self.snake_board.G_HEIGHT//self.snake_board.WRES)) * self.snake_board.WRES] #create new food
        else:
            self.body_snake.pop() #just move snake

    def _check_gameover(self): # check if any violation occurRED
        # Touched the wall
        if (self.pos_snake[0] < 0 or self.pos_snake[0] > self.snake_board.G_WIDTH-self.snake_board.WRES) or self.pos_snake[1] < 0 or self.pos_snake[1] > self.snake_board.G_HEIGHT-self.snake_board.WRES:
            return True

        # Touched the snake body
        for block in self.body_snake[1:]:
            if self.pos_snake[0] == block[0] and self.pos_snake[1] == block[1]:
                return True
            
        return False # No violation
    
    """
    def _show_updated_score(self): # displaying Score function
        # creating font object score_font
        score_font = pygame.font.SysFont('times new roman', 12)
        
        # create the display surface object 
        # score_surface
        score_surface = score_font.render('Score : ' + str(self.score), True, (255,255,255))
        
        # create a rectangular object for the text
        # surface object
        score_rect = score_surface.get_rect()
        
        # displaying text
        self.game_window.blit(score_surface, score_rect)
    """
    
    #endregion