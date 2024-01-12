# importing libraries
import pygame
import random
import numpy as np
import math

class SnakeGame:

#region ----- Class variables -----
#endregion

#region ----- Methods -----

    def __init__(self, snake_board):
        print("SnakeGame instance created.")
        self.snake_board = snake_board
        self._init_game()

    def step_game(self, req_dir = "IDLE"):
        # Run game and update state / score if not game over
        if self.game_over == False:
            self._update_game_state(req_dir)
        #self._show_updated_score()

        # Check for game-over condition
        self.game_over = self._check_gameover()

        # Return game score and status
        return [self.game_over, self.score] # Game-over + score
    
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

    def reset_game(self):
        self._init_game()

    def _init_game(self):
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
        self.timeout = (self.snake_board.G_HEIGHT * self.snake_board.G_WIDTH)/(self.snake_board.WRES)**2

    def get_game_state(self):
        # ----- Calc food angle regarding snake's head and current direction -----
        # Normal cartesian coordinates, based on a snake going to the right
        dx_std = (self.pos_food[0] - self.pos_snake[0])  # x-axis grow left-right
        dy_std = ((self.pos_food[1] - self.pos_snake[1]) * -1 ) # y-axis grow top-down

        # Adjust axis rotation reference
        if self.direction == "RIGHT":
            dx = dx_std
            dy = dy_std
        elif self.direction == "UP":
            dx = dy_std
            dy = -dx_std
        elif self.direction == "LEFT":
            dx = -dx_std
            dy = -dy_std
        elif self.direction == "DOWN":
            dx = -dy_std
            dy = dx_std

        food_angle = math.atan2(dy,dx) / (math.pi)
        return [food_angle]

    def _update_game_state(self, req_dir):
        # Validate new requested direction - HEAD BASED
        if req_dir == 'T_LEFT' and self.direction == 'UP':
            self.direction = 'LEFT'
        elif req_dir == 'T_LEFT' and self.direction == 'DOWN':
            self.direction = 'RIGHT'
        elif req_dir == 'T_LEFT' and self.direction == 'LEFT':
            self.direction = 'DOWN'
        elif req_dir == 'T_LEFT' and self.direction == 'RIGHT':
            self.direction = 'UP'
        
        elif req_dir == 'T_RIGHT' and self.direction == 'UP':
            self.direction = 'RIGHT'
        elif req_dir == 'T_RIGHT' and self.direction == 'DOWN':
            self.direction = 'LEFT'
        elif req_dir == 'T_RIGHT' and self.direction == 'LEFT':
            self.direction = 'UP'
        elif req_dir == 'T_RIGHT' and self.direction == 'RIGHT':
            self.direction = 'DOWN'

        # Validate new requested direction - BOARD BASED
        else:
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
            self.timeout = (self.snake_board.G_HEIGHT * self.snake_board.G_WIDTH)/(self.snake_board.WRES)**2
        else:
            self.body_snake.pop() #just move snake
            self.timeout = self.timeout -1

    def _check_gameover(self): # check if any violation ocurred
        # Touched the wall
        if (self.pos_snake[0] < 0 or self.pos_snake[0] > self.snake_board.G_WIDTH-self.snake_board.WRES) or self.pos_snake[1] < 0 or self.pos_snake[1] > self.snake_board.G_HEIGHT-self.snake_board.WRES:
            return True

        # Touched the snake body
        for block in self.body_snake[1:]:
            if self.pos_snake[0] == block[0] and self.pos_snake[1] == block[1]:
                return True

        if self.timeout <= 0:
            print("TIMEOUT")
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