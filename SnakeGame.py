# importing libraries
import random
import math
import numpy as np

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
        #self.pos_snake = np.array([2,2])
        self.pos_snake = [2,2]
        #self.pos_snake = [1,3]

        # defining first blocks of snake body
        #self.body_snake = np.array([[2, 2], [1, 2]])
        self.body_snake = [[2, 2], [1, 2]]
        
        #self.body_snake = [[1, 3], [0, 3], [0, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [4, 4], [4, 3], [4, 2],[4,1]]
        
        # fruit position
        self.pos_food = [random.randrange(1, (self.board_size)), random.randrange(1, (self.board_size))]

        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.score = 0 # initial score
        self.w_score = 0 # weighed score
        self.game_over = False
        self.timeout = (2*self.board_size*self.board_size)

    def step_game(self, req_dir = "IDLE"):
        # Run game and update state / score if not game over
        if self.game_over == False:
            self._update_game_state(req_dir)

        # Check for game-over condition
        self.game_over = self._check_gameover()

        # Return game score and status
        return [self.game_over, self.w_score, self.score] # Game-over + score
    
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
        
        #food_angle = round(food_angle/0.25) * 0.25 # Truncate

        # ----- Calc hazards distance -----          
        # Distance to walls - Absolute coordinates (don't care about snake's direction)
        # Left, Right, Up and Down respectively
        h2l_wall = self.pos_snake[0] / (self.board_size-1) # h2lw -> head to left wall
        h2r_wall = 1 - h2l_wall # h2rw -> head to right wall
        h2u_wall = self.pos_snake[1] / (self.board_size-1) # h2uw -> head to upper wall
        h2d_wall = 1 - h2u_wall # h2dw -> head to lower (down) wall
        # Diagonals
        h2lu_wall = min(h2l_wall, h2u_wall)
        h2ld_wall = min(h2l_wall, h2d_wall)
        h2ru_wall = min(h2r_wall, h2u_wall)
        h2rd_wall = min(h2r_wall, h2d_wall)

        # Distance to body - Absolute coordinates (don't care about snake's direction)
        body = np.array(self.body_snake, dtype=int)
        head = np.array(self.pos_snake, dtype=int)
        
        # Distance from snake head to body parts
        dist_body = (head-body)

        # values that share same X (vertically distant)
        vdist_body = dist_body[dist_body[:,0]==0]#.flatten()

        # values that share same Y (horizontally distant)
        hdist_body = dist_body[dist_body[:,1]==0]#.flatten()

        # values that are in the diagonals
        ddist_body = dist_body[abs(dist_body[:,1]) == abs(dist_body[:,0])]
        
        # consolidate distance values in individual normalized variables
        norm_board = 1/(self.board_size-1)
        
        h2u_body =  (np.min(vdist_body[vdist_body > 0])-1)*norm_board \
                if vdist_body[vdist_body > 0].size > 0 \
                else h2u_wall
        h2d_body =  -1*((np.max(vdist_body[vdist_body < 0]))+1)*norm_board \
                if vdist_body[vdist_body < 0].size > 0 \
                else h2d_wall
        h2l_body =  (np.min(hdist_body[hdist_body > 0])-1)*norm_board \
                if hdist_body[hdist_body > 0].size > 0 \
                else h2l_wall
        h2r_body =  -1*(np.max(hdist_body[hdist_body < 0])+1)*norm_board \
                if hdist_body[hdist_body < 0].size > 0 \
                else h2r_wall
        
        h2ru_body = (np.min(np.abs(ddist_body[(ddist_body[:,0] < 0) & (ddist_body[:,1] > 0)]))-1)*norm_board \
                if ddist_body[(ddist_body[:,0] < 0) & (ddist_body[:,1] > 0)].size > 0 \
                else h2ru_wall
        h2rd_body = (np.min(np.abs(ddist_body[(ddist_body[:,0] < 0) & (ddist_body[:,1] < 0)]))-1)*norm_board \
                if ddist_body[(ddist_body[:,0] < 0) & (ddist_body[:,1] < 0)].size > 0 \
                else h2rd_wall
        h2lu_body = (np.min(np.abs(ddist_body[(ddist_body[:,0] > 0) & (ddist_body[:,1] > 0)]))-1)*norm_board \
                if ddist_body[(ddist_body[:,0] > 0) & (ddist_body[:,1] > 0)].size > 0 \
                else h2lu_wall 
        h2ld_body = (np.min(np.abs(ddist_body[(ddist_body[:,0] > 0) & (ddist_body[:,1] < 0)]))-1)*norm_board \
                if ddist_body[(ddist_body[:,0] > 0) & (ddist_body[:,1] < 0)].size > 0 \
                else h2ld_wall        
        
        # Distance to hazard - min between wall and body - relative coordinates (based on snake's direction)
        if self.direction == "RIGHT":
            haz_ahead = h2r_body #Abs Right
            haz_left = h2u_body #Abs Up
            haz_right = h2d_body #Abs Dw
            haz_ahead_left = h2ru_body
            haz_ahead_right = h2rd_body
            haz_behind_left = h2lu_body
            haz_behind_right = h2ld_body
        elif self.direction == "UP":
            haz_ahead = h2u_body
            haz_left = h2l_body 
            haz_right = h2r_body 
            haz_ahead_left = h2lu_body
            haz_ahead_right = h2ru_body
            haz_behind_left = h2ld_body
            haz_behind_right = h2rd_body
        elif self.direction == "LEFT":
            haz_ahead = h2l_body 
            haz_left = h2d_body 
            haz_right = h2u_body 
            haz_ahead_left = h2ld_body
            haz_ahead_right = h2lu_body
            haz_behind_left = h2rd_body
            haz_behind_right = h2ru_body
        elif self.direction == "DOWN":
            haz_ahead = h2d_body 
            haz_left = h2r_body 
            haz_right = h2l_body 
            haz_ahead_left = h2rd_body
            haz_ahead_right = h2ld_body
            haz_behind_left = h2ru_body
            haz_behind_right = h2lu_body
       
        return [+1 if food_angle>0 else (0 if np.abs(food_angle) < 1e-2 else -1), 
                -1 if np.abs(food_angle) > 0.501 else (0 if np.abs(food_angle) > 0.499 and np.abs(food_angle) < 0.501 else 1),
                +1 if haz_ahead==0 else 0,
                +1 if haz_left==0 else 0,
                +1 if haz_right==0 else 0, 
                +1 if haz_ahead_left==0 else 0, 
                +1 if haz_ahead_right==0 else 0, 
                +1 if haz_behind_left==0 else 0, 
                +1 if haz_behind_right==0 else 0]

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
        #self.body_snake= np.vstack((self.body_snake, self.pos_snake))
        
        if self.pos_snake[0] == self.pos_food[0] and self.pos_snake[1] == self.pos_food[1]:
            self.score += 1 # grow snake
            self.w_score += self.timeout # receive remaining time as energy

            # Create a new food in an available position        
            available_positions = {(x, y) for x in range(self.board_size) for y in range(self.board_size)} - set(map(tuple, self.body_snake))
            if available_positions:
                self.pos_food = random.choice(list(available_positions))
            else:
                # TODO: Unreachable - just placed here for catching any unpredicted condition.
                print("No available position for food insertion") 

            self.timeout = (2*self.board_size*self.board_size)
        else:
            #just move snake
            self.body_snake.pop()
            # self.body_snake = np.delete(self.body_snake, [0], axis =0) 
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
            #print(f"Game over - Max score of {self.score} achieved!")
            return True

        if self.timeout <= 0:
            return True
        
        return False # No violation
    
#endregion