# importing libraries
import pygame
import time
import random
import numpy as np
import os

class SnakeGame:

#region ----- Class variables -----
    # defining colors
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)

    G_SPD = 10 # game speed up to 10fps

    # Window size (always a multiple of 10)
    WRES = 5
    G_WIDTH = 20 * WRES
    G_HEIGHT = 20 * WRES
    S_WIDTH = 1368
    S_HEIGHT = 768

    AUTO_RESTART = False
    WAIT_TRANS = 1
#endregion

#region ----- Methods -----

    def __init__(self,pos):
        print("SnakeGame instance created.")
        self.start_game = 1
        self.pos = pos

    def init_game(self):
        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()
        
        # Initializing pygame window in correct position
        y = np.floor(self.pos * SnakeGame.G_WIDTH/ (SnakeGame.S_WIDTH*0.8)) * SnakeGame.G_HEIGHT * 1.1
        x = (self.pos * SnakeGame.G_WIDTH) - (np.floor(self.pos* SnakeGame.G_WIDTH/(SnakeGame.S_WIDTH*0.8)) * (SnakeGame.S_WIDTH*0.8))
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
        pygame.init()

        # Initialize game window
        pygame.display.set_caption('Snake Game')
        self.game_window = pygame.display.set_mode((SnakeGame.G_WIDTH, SnakeGame.G_HEIGHT))

        # defining snake default position
        self.pos_snake = [1*SnakeGame.WRES, 1*SnakeGame.WRES]

        # defining first 4 blocks of snake body
        self.body_snake = [[1*SnakeGame.WRES, 1*SnakeGame.WRES], [0*SnakeGame.WRES, 1*SnakeGame.WRES]]
        
        # fruit position
        self.pos_food = [random.randrange(1, (SnakeGame.G_WIDTH//SnakeGame.WRES)) * SnakeGame.WRES, 
                        random.randrange(1, (SnakeGame.G_HEIGHT//SnakeGame.WRES)) * SnakeGame.WRES]

        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.score = 0 # initial score

    def step_game(self, req_dir = "IDLE"):
        # Auto-start game if needed
        if self.start_game == 1:
            self.init_game()
            self.start_game=0

        # Run game and update score
        self._update_board_elements(req_dir)
        self._show_updated_score()

        # Check for game-over condition
        game_over = self._check_gameover()
        if game_over == 1: 
            time.sleep(SnakeGame.WAIT_TRANS)
            self.start_game=1
            if SnakeGame.AUTO_RESTART == False:
                self.quit_game()
        else:
            # Refresh game screen
            pygame.display.update()

            # Frame Per Second / Refresh Rate
            self.fps.tick(SnakeGame.G_SPD)

        # Get game state
        state = self.get_game_state()
            

        return [game_over, state, self.score] # Game-over + score
    
    def get_game_state(self):
        food_up = 1 if self.pos_snake[1] > self.pos_food[1] else 0
        food_dw = 1 if self.pos_snake[1] < self.pos_food[1] else 0
        food_left = 1 if self.pos_snake[0] > self.pos_food[0] else 0
        food_right = 1 if self.pos_snake[0] < self.pos_food[0] else 0

        dir_up = 1 if self.direction == 'UP' else 0
        dir_down = 1 if self.direction == 'DOWN' else 0
        dir_left = 1 if self.direction == 'LEFT' else 0
        dir_right = 1 if self.direction == 'RIGHT' else 0

        wall_up = 1 if self.pos_snake[1] == 0 else 0
        wall_down = 1 if self.pos_snake[1] == (SnakeGame.G_HEIGHT -  SnakeGame.WRES) else 0
        wall_left = 1 if self.pos_snake[0] == 0 else 0
        wall_right = 1 if self.pos_snake[0] == (SnakeGame.G_WIDTH -  SnakeGame.WRES) else 0   
        
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
    
    def quit_game(self):
        pygame.quit()

    def _update_board_elements(self, req_dir):
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
            self.pos_snake[1] -= SnakeGame.WRES
        if self.direction == 'DOWN':
            self.pos_snake[1] += SnakeGame.WRES
        if self.direction == 'LEFT':
            self.pos_snake[0] -= SnakeGame.WRES
        if self.direction == 'RIGHT':
            self.pos_snake[0] += SnakeGame.WRES

        # Check if snake shall eat the food
        self.body_snake.insert(0, list(self.pos_snake))
        if self.pos_snake[0] == self.pos_food[0] and self.pos_snake[1] == self.pos_food[1]:
            self.score += 1 # grow snake
            self.pos_food = [random.randrange(1, (SnakeGame.G_WIDTH//SnakeGame.WRES)) * SnakeGame.WRES,
                                random.randrange(1, (SnakeGame.G_HEIGHT//SnakeGame.WRES)) * SnakeGame.WRES] #create new food
        else:
            self.body_snake.pop() #just move snake

        # Refresh game board
        self.game_window.fill(SnakeGame.BLACK) 
        for pos in self.body_snake: # draw snake
            pygame.draw.rect(self.game_window, SnakeGame.GREEN, pygame.Rect(pos[0], pos[1], SnakeGame.WRES, SnakeGame.WRES))
		
        # draw food
        pygame.draw.rect(self.game_window, SnakeGame.WHITE, pygame.Rect(self.pos_food[0], self.pos_food[1], SnakeGame.WRES, SnakeGame.WRES))
		
    def _check_gameover(self): # check if any violation occurRED
        # game over function
        def _game_over_msg():
            # creating font object my_font
            my_font = pygame.font.SysFont('times new roman', 12)
            
            # creating a text surface on which text will be drawn
            game_over_surface = my_font.render(' Your score is : ' + str(self.score) + ' ', True, SnakeGame.RED, (255,255,255,100))
            
            # create a rectangular object for the text surface object
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.midtop = (SnakeGame.G_WIDTH/2, SnakeGame.G_HEIGHT/2) # setting position of the text

            # blit will draw the text on screen
            self.game_window.blit(game_over_surface, game_over_rect)
            pygame.display.flip()            

        # Touched the wall
        if (self.pos_snake[0] < 0 or self.pos_snake[0] > SnakeGame.G_WIDTH-SnakeGame.WRES) or self.pos_snake[1] < 0 or self.pos_snake[1] > SnakeGame.G_HEIGHT-SnakeGame.WRES:
            _game_over_msg()
            return True

        # Touched the snake body
        for block in self.body_snake[1:]:
            if self.pos_snake[0] == block[0] and self.pos_snake[1] == block[1]:
                _game_over_msg()
                return True
            
        return False # No violation
    
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
    
    #endregion