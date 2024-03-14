# importing libraries
import pygame
import random
import math

class SnakeGame:

#region ----- Class variables -----
#endregion

#region ----- Methods -----

    def __init__(self, snake_board):
        #print("SnakeGame instance created.")
        self.snake_board = snake_board
        self._init_game()

    def step_game(self, req_dir = "IDLE"):
        # Run game and update state / score if not game over
        if self.game_over == False:
            self._update_game_state(req_dir)

        # Check for game-over condition
        self.game_over = self._check_gameover()

        # Return game score and status
        return [self.game_over, self.w_score, self.score] # Game-over + score
    
    def get_key(self):
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
        self.pos_snake = [2,2]

        # defining first blocks of snake body
        self.body_snake = [[2, 2], [1, 2]]
        
        # fruit position
        self.pos_food = [random.randrange(1, (self.snake_board.G_WIDTH)), random.randrange(1, (self.snake_board.G_HEIGHT))]

        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.score = 0 # initial score
        self.w_score = 0 # weighed score
        self.game_over = False
        self.timeout = (self.snake_board.G_HEIGHT * self.snake_board.G_WIDTH)

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

        # ----- Calc hazards distance -----
        # Distance to walls 
        rel_pos_x = (self.snake_board.G_WIDTH - 1 - self.pos_snake[0]) / (self.snake_board.G_WIDTH-1)
        rel_pos_y = (self.snake_board.G_HEIGHT- 1 - self.pos_snake[1]) / (self.snake_board.G_HEIGHT-1)

        if self.direction == "RIGHT":
            rel_pos_ahead_wall = rel_pos_x
            rel_pos_lat_wall = 1-rel_pos_y
        elif self.direction == "UP":
            rel_pos_ahead_wall = 1-rel_pos_y
            rel_pos_lat_wall = 1-rel_pos_x
        elif self.direction == "LEFT":
            rel_pos_ahead_wall = 1-rel_pos_x
            rel_pos_lat_wall = rel_pos_y
        elif self.direction == "DOWN":
            rel_pos_ahead_wall = rel_pos_y
            rel_pos_lat_wall = rel_pos_x

        #print("X / Y:", self.pos_snake[0], "  -  ", self.pos_snake[1])
        #print("AHEAD: ", rel_pos_ahead_wall, " - LAT: ", rel_pos_lat_wall)

        # Distance to body
        d_body_x = [self.snake_board.G_WIDTH, -1*self.snake_board.G_WIDTH]
        d_body_y = [self.snake_board.G_WIDTH, -1*self.snake_board.G_WIDTH]
        for block in self.body_snake[1:]:
            if block[0] == self.pos_snake[0]:
                d_body_y.append(block[1] - self.pos_snake[1])
            if block[1] == self.pos_snake[1]:
                d_body_x.append(block[0] - self.pos_snake[0])

        if self.direction == "RIGHT":
            d_ahead = min([i for i in d_body_x if i > 0])
            d_lat = min(d_body_y, key=lambda x: abs(x))
        elif self.direction == "UP":
            d_ahead = min([i for i in d_body_y if i < 0]) 
            d_lat = min(d_body_x, key=lambda x: abs(x))       
        elif self.direction == "LEFT":
            d_ahead = min([i for i in d_body_x if i < 0])
            d_lat = -1 * min(d_body_y, key=lambda x: abs(x))
        elif self.direction == "DOWN":
            d_ahead = min([i for i in d_body_y if i > 0])
            d_lat = -1 * min(d_body_x, key=lambda x: abs(x))

        rel_pos_ahead_body = d_ahead / self.snake_board.G_WIDTH
        rel_pos_lat_body = d_lat / self.snake_board.G_WIDTH
        #print("AHEAD: ", rel_pos_ahead_body, " - LAT: ", rel_pos_lat_body)

        return [food_angle, rel_pos_ahead_wall, rel_pos_lat_wall, rel_pos_ahead_body, rel_pos_lat_body]

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
            self.pos_snake[1] -= 1
        if self.direction == 'DOWN':
            self.pos_snake[1] += 1
        if self.direction == 'LEFT':
            self.pos_snake[0] -= 1
        if self.direction == 'RIGHT':
            self.pos_snake[0] += 1

        # Check if snake shall eat the food
        self.body_snake.insert(0, list(self.pos_snake))
        if self.pos_snake[0] == self.pos_food[0] and self.pos_snake[1] == self.pos_food[1]:
            self.score += 1 # grow snake
            self.w_score += self.timeout # received remaining time as energy
            
            while True: # Randomize until food doesn't overlap snake's body
                self.pos_food = [random.randrange(1, (self.snake_board.G_WIDTH)) , random.randrange(1, (self.snake_board.G_HEIGHT)) ] #create new food
                non_overlap = 1
                for block in self.body_snake:
                    if block[0] == self.pos_food[0] and block[1] == self.pos_food[1]:
                        non_overlap = 0
                        break
                if non_overlap == 1:
                    break

            self.timeout = (self.snake_board.G_HEIGHT * self.snake_board.G_WIDTH)
        else:
            self.body_snake.pop() #just move snake
            self.timeout = self.timeout - 1

    def _check_gameover(self): # check if any violation ocurred
        # Touched the wall
        if (self.pos_snake[0] < 0 or self.pos_snake[0] > self.snake_board.G_WIDTH-1) or self.pos_snake[1] < 0 or self.pos_snake[1] > self.snake_board.G_HEIGHT-1:
            return True

        # Touched the snake body
        for block in self.body_snake[1:]:
            if self.pos_snake[0] == block[0] and self.pos_snake[1] == block[1]:
                return True

        if self.timeout <= 0:
            #print("TIMEOUT")
            return True
        
        return False # No violation
    
    #endregion