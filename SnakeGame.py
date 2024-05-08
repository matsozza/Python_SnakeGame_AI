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
        #food_distance = math.sqrt(abs(dx_std)**2 + abs(dy_std)**2) / math.sqrt((self.snake_board.G_HEIGHT-1)**2 + (self.snake_board.G_WIDTH-1)**2)

        # ----- Calc hazards distance -----
        MAXCOORD = self.snake_board.G_HEIGHT # Assuming square table
        
        # Distance to walls - Absolute coordinates (don't care about snake's direction)
        h2lw = self.pos_snake[0] / (MAXCOORD-1) # h2lw -> head to left wall
        h2rw = 1 - h2lw # h2rw -> head to right wall
        h2uw = self.pos_snake[1] / (MAXCOORD-1) # h2uw -> head to upper wall
        h2dw = 1 - h2uw # h2dw -> head to lower (down) wall

        # Distance to body - Absolute coordinates (don't care about snake's direction)
        h2lb, h2rb, h2ub, h2db = h2lw, h2rw, h2uw, h2dw
        for i in range(1,MAXCOORD-2):
            # Break loop if distances will be no more updated - minimum found
            if h2lb <= (i-1) and h2rb <= (i-1) and h2ub <= (i-1) and h2db <= (i-1):
                break

            for j, body in enumerate(self.body_snake):
                # Check head to body distance to the left (absolute coord)
                if self.pos_snake[0] == body[0]+i and self.pos_snake[1] == body[1]:
                    h2lb = min(h2lb, (i-1) / (MAXCOORD-1))
                # Check head to body distance to the right (absolute coord)
                elif self.pos_snake[0] == body[0]-i and self.pos_snake[1] == body[1]:
                    h2rb = min(h2rb, (i-1) / (MAXCOORD-1))
                # Check head to body distance to above (absolute coord)
                elif self.pos_snake[0] == body[0] and self.pos_snake[1] == body[1]+i:
                    h2ub = min(h2ub, (i-1) / (MAXCOORD-1))
                # Check head to body distance to below (absolute coord)
                elif self.pos_snake[0] == body[0] and self.pos_snake[1] == body[1]-i:
                    h2db = min(h2db, (i-1) / (MAXCOORD-1))
            

        # Distance to hazard - min between wall and body - relative coordinates (based on snake's direction)
        if self.direction == "RIGHT":
            haz_ahead = min(h2rw, h2rb) #Abs Right
            haz_left = min(h2uw, h2ub) #Abs Up
            haz_right = min(h2dw, h2db) #Abs Dw
        elif self.direction == "UP":
            haz_ahead = min(h2uw, h2ub) 
            haz_left = min(h2lw, h2lb) 
            haz_right = min(h2rw, h2rb) 
        elif self.direction == "LEFT":
            haz_ahead = min(h2lw, h2lb) 
            haz_left = min(h2dw, h2db) 
            haz_right = min(h2uw, h2ub) 
        elif self.direction == "DOWN":
            haz_ahead = min(h2dw, h2db) 
            haz_left = min(h2rw, h2rb) 
            haz_right = min(h2lw, h2lb) 
        
        #print(f'AHEAD: {haz_ahead} --- left: {haz_left} --- right: {haz_right}')

        return [food_angle, haz_ahead, haz_left, haz_right]

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
        
        # Calculate new snake head position
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
            self.w_score += self.timeout # receive remaining time as energy
            
            # Create a new food - Randomize until food doesn't overlap snake's body
            idxFoodLoop = 0
            while True: 
                self.pos_food = [random.randrange(0, (self.snake_board.G_WIDTH)) , random.randrange(0, (self.snake_board.G_HEIGHT)) ] #create new food
                non_overlap = 1
                for block in self.body_snake:
                    if block[0] == self.pos_food[0] and block[1] == self.pos_food[1]:
                        non_overlap = 0
                        break
                if non_overlap == 1:
                    break
                idxFoodLoop= idxFoodLoop+1
                if idxFoodLoop > 30:
                    print("Food loop taking too long - ", idxFoodLoop, " - Snake size: ", self.score)

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
            
        # Snake achieved maximum size possible
        if self.score == (self.snake_board.G_WIDTH * self.snake_board.G_HEIGHT) - 3:
            print(" Game over - Max size achieved!")
            return True

        if self.timeout <= 0:
            #print("TIMEOUT")
            return True
        
        return False # No violation
    
    #endregion