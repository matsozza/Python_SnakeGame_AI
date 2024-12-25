# importing libraries
import pygame
import random
import math

class SnakeGame:

#region ----- Class variables -----

#endregion

#region ----- Methods -----

    def __init__(self, board_size = 6):
        #print("SnakeGame instance created.")
        self.board_size = board_size
        self._init_game()
    
    def _init_game(self):
        # defining snake initial position
        self.pos_snake = [2,2]
        #self.pos_snake = [1,3]

        # defining first blocks of snake body
        self.body_snake = [[2, 2], [1, 2]]
        #self.body_snake = [[1, 3], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [4, 4], [4, 3], [4, 2],[4,1]]
        
        # fruit position
        self.pos_food = [random.randrange(1, (self.board_size)), random.randrange(1, (self.board_size))]

        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.score = 0 # initial score
        self.w_score = 0 # weighed score
        self.game_over = False
        self.timeout = (self.board_size * self.board_size)

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
                if event.key == pygame.K_p:
                    return 'PAUSE'
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
        food_angle = round((math.atan2(dy,dx) / (math.pi)),2)
        #food_distance = math.sqrt(abs(dx_std)**2 + abs(dy_std)**2) / math.sqrt((self.board_size-1)**2 + (self.board_size-1)**2)

        # ----- Calc hazards distance -----
        MAXCOORD = self.board_size # Assuming square table
        
        # Distance to walls - Absolute coordinates (don't care about snake's direction)
        # Left, Right, Up and Down respectively
        h2l_wall = self.pos_snake[0] / (MAXCOORD-1) # h2lw -> head to left wall
        h2r_wall = 1 - h2l_wall # h2rw -> head to right wall
        h2u_wall = self.pos_snake[1] / (MAXCOORD-1) # h2uw -> head to upper wall
        h2d_wall = 1 - h2u_wall # h2dw -> head to lower (down) wall
        # Diagonals
        h2lu_wall = min(h2l_wall, h2u_wall)
        h2ld_wall = min(h2l_wall, h2d_wall)
        h2ru_wall = min(h2r_wall, h2u_wall)
        h2rd_wall = min(h2r_wall, h2d_wall)

        # Distance to body - Absolute coordinates (don't care about snake's direction)
        # Values are started based on distance to wall values (worst case)
        h2l_body, h2r_body, h2u_body, h2d_body = h2l_wall, h2r_wall, h2u_wall, h2d_wall
        h2lu_body, h2ld_body, h2ru_body, h2rd_body = h2lu_wall, h2ld_wall, h2ru_wall, h2rd_wall
        for i in range(1,MAXCOORD-2):
            # Break loop if distances will be no more updated - minimum already found
            if h2l_body <= (i-1)/(MAXCOORD-1) and h2r_body <= (i-1)/(MAXCOORD-1) and \
               h2u_body <= (i-1)/(MAXCOORD-1) and h2d_body <= (i-1)/(MAXCOORD-1):
                break

            for _, body in enumerate(self.body_snake):
                # Check head to body distance - left (absolute coord)
                if self.pos_snake[0] == body[0]+i and self.pos_snake[1] == body[1]:
                    h2l_body = min(h2l_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - right (absolute coord)
                elif self.pos_snake[0] == body[0]-i and self.pos_snake[1] == body[1]:
                    h2r_body = min(h2r_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - above (absolute coord)
                elif self.pos_snake[0] == body[0] and self.pos_snake[1] == body[1]+i:
                    h2u_body = min(h2u_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - below (absolute coord)
                elif self.pos_snake[0] == body[0] and self.pos_snake[1] == body[1]-i:
                    h2d_body = min(h2d_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - diag above / left
                elif self.pos_snake[0] == body[0]+i and self.pos_snake[1]==body[1]+i:
                    h2lu_body = min(h2lu_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - diag below / left
                elif self.pos_snake[0] == body[0]+i and self.pos_snake[1]==body[1]-i:
                    h2ld_body = min(h2ld_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - diag above / right
                elif self.pos_snake[0] == body[0]-i and self.pos_snake[1]==body[1]+i:
                    h2ru_body = min(h2ru_body, (i-1) / (MAXCOORD-1))
                # Check head to body distance - diag below / right
                elif self.pos_snake[0] == body[0]-i and self.pos_snake[1]==body[1]-i:
                    h2rd_body = min(h2rd_body, (i-1) / (MAXCOORD-1))
                    
        # Distance to hazard - min between wall and body - relative coordinates (based on snake's direction)
        if self.direction == "RIGHT":
            haz_ahead = min(h2r_wall, h2r_body) #Abs Right
            haz_left = min(h2u_wall, h2u_body) #Abs Up
            haz_right = min(h2d_wall, h2d_body) #Abs Dw
            haz_ahead_left = min(h2ru_wall, h2ru_body)
            haz_ahead_right = min(h2rd_wall, h2rd_body)
        elif self.direction == "UP":
            haz_ahead = min(h2u_wall, h2u_body) 
            haz_left = min(h2l_wall, h2l_body) 
            haz_right = min(h2r_wall, h2r_body) 
            haz_ahead_left = min(h2lu_wall, h2lu_body)
            haz_ahead_right = min(h2ru_wall, h2ru_body)
        elif self.direction == "LEFT":
            haz_ahead = min(h2l_wall, h2l_body) 
            haz_left = min(h2d_wall, h2d_body) 
            haz_right = min(h2u_wall, h2u_body) 
            haz_ahead_left = min(h2ld_wall, h2ld_body)
            haz_ahead_right = min(h2lu_wall, h2lu_body)
        elif self.direction == "DOWN":
            haz_ahead = min(h2d_wall, h2d_body) 
            haz_left = min(h2r_wall, h2r_body) 
            haz_right = min(h2l_wall, h2l_body) 
            haz_ahead_left = min(h2rd_wall, h2rd_body)
            haz_ahead_right = min(h2ld_wall, h2ld_body)
        
        #print(f'Food Angle: {180*food_angle} -- Haz. Ahead: {haz_ahead} -- Haz. Left: {haz_left} -- Haz. Right: {haz_right}\n Haz. Ah-Left: {haz_ahead_left} -- Haz. Ah-Right: {haz_ahead_right}')

        return [food_angle, haz_ahead, haz_left, haz_right, haz_ahead_left, haz_ahead_right]

    def _update_game_state(self, req_dir):
        # Input validation  - If number provided, map to textual
        if req_dir == 0: req_dir = "IDLE"
        elif req_dir == 1: req_dir = "T_LEFT"
        elif req_dir == 2: req_dir = "T_RIGHT"

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
            elif req_dir == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            elif req_dir == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            elif req_dir == 'RIGHT' and self.direction != 'LEFT':
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
                self.pos_food = [random.randrange(0, (self.board_size)) , random.randrange(0, (self.board_size)) ] #create new food
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

            self.timeout = (self.board_size * self.board_size)
        else:
            self.body_snake.pop() #just move snake
            self.timeout = self.timeout - 1

    def _check_gameover(self):
        # Touched the wall
        if (self.pos_snake[0] < 0 or self.pos_snake[0] > self.board_size-1) or self.pos_snake[1] < 0 or self.pos_snake[1] > self.board_size-1:
            return True

        # Touched the snake body
        for block in self.body_snake[1:]:
            if self.pos_snake[0] == block[0] and self.pos_snake[1] == block[1]:
                return True
            
        # Snake achieved maximum size possible
        if self.score == (self.board_size * self.board_size) - 3:
            print(f"Game over - Max score of {self.score} achieved!")
            return True

        if self.timeout <= 0:
            return True
        
        return False # No violation
    
#endregion