# importing libraries
import pygame
import time
import random
#import neural_network
import numpy as np
import os

# Main Function
def run_game_w(args):
    return run_game(*args)

def run_game(model, pos):
	global change_to, direction, fruit_position, fruit_spawn, score
	init_game(pos)
	while True:
		req_dir = _get_key() # Manual mode / Exit game
		[go, score] = step_game()

		if go == True:
			init_game(pos)

def step_game():
	_update_snake_food()
	_show_updated_score()
	go = _check_gameover()

	# Refresh game screen
	pygame.display.update()

	# Frame Per Second / Refresh Rate
	fps.tick(G_SPD)

	return [go, score] # Game-over + score

def init_game(pos):
	global change_to, direction, fruit_position, fruit_spawn, score, snake_position, snake_body, game_window, BLACK, WHITE, RED,GREEN,BLUE,quantum, window_x,window_y,fps, G_SPD

	# FPS (frames per second) controller
	fps = pygame.time.Clock()
	G_SPD = 10 # game speed up to 10fps

	# Window size (always a multiple of 10)
	quantum = 5
	window_x = 25 * quantum
	window_y = 25 * quantum
	S_WIDTH = 1368
	S_HEIGHT = 768

	# defining colors
	BLACK = pygame.Color(0, 0, 0)
	WHITE = pygame.Color(255, 255, 255)
	RED = pygame.Color(255, 0, 0)
	GREEN = pygame.Color(0, 255, 0)
	BLUE = pygame.Color(0, 0, 255)

	# Initializing pygame in correct position
	y = np.floor(pos * window_x/ (S_WIDTH*0.8)) * window_y * 1.1
	x = (pos * window_x) - (np.floor(pos* window_x/(S_WIDTH*0.8)) * (S_WIDTH*0.8))
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
	pygame.init()

	# Initialize game window
	pygame.display.set_caption('Snake Game')
	game_window = pygame.display.set_mode((window_x, window_y))

	# defining snake default position
	snake_position = [10*quantum, 5*quantum]

	# defining first 4 blocks of snake body
	snake_body = [[10*quantum, 5*quantum], [9*quantum, 5*quantum]]
	# fruit position
	fruit_position = [random.randrange(1, (window_x//quantum)) * quantum, 
					random.randrange(1, (window_y//quantum)) * quantum]

	# setting default snake direction towards right
	direction = 'RIGHT'
	change_to = direction

	score = 0 # initial score

def _get_key():
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

def _update_snake_food():
		global fruit_position, fruit_spawn, snake_body, snake_position, fruit_position, quantum, window_x, window_y, game_window, WHITE, GREEN, score

		# Calculate new snake position
		if direction == 'UP':
			snake_position[1] -= quantum
		if direction == 'DOWN':
			snake_position[1] += quantum
		if direction == 'LEFT':
			snake_position[0] -= quantum
		if direction == 'RIGHT':
			snake_position[0] += quantum
		
		# Check if snake shall eat the food
		snake_body.insert(0, list(snake_position))
		if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
			score += 1 # grow snake
			fruit_position = [random.randrange(1, (window_x//quantum)) * quantum,
					 		 random.randrange(1, (window_y//quantum)) * quantum] #create new food
		else:
			snake_body.pop() #just move snake
	
		# Refresh game board
		game_window.fill(BLACK) 
		for pos in snake_body: # draw snake
			pygame.draw.rect(game_window, GREEN,pygame.Rect(pos[0], pos[1], quantum, quantum))
		
		# draw food
		pygame.draw.rect(game_window, WHITE, pygame.Rect(fruit_position[0], fruit_position[1], quantum, quantum))

def _check_gameover(): # check if any violation occurRED
	# game over function
	def _game_over_msg():
		# creating font object my_font
		my_font = pygame.font.SysFont('times new roman', 12)
		
		# creating a text surface on which text will be drawn
		game_over_surface = my_font.render(' Your Score is : ' + str(score) + ' ', True, RED, (255,255,255,100))
		
		# create a rectangular object for the text surface object
		game_over_rect = game_over_surface.get_rect()
		game_over_rect.midtop = (window_x/2, window_y/2) # setting position of the text

		# blit will draw the text on screen
		game_window.blit(game_over_surface, game_over_rect)
		pygame.display.flip()
		
		time.sleep(2)

	# Touched the wall
	if (snake_position[0] < 0 or snake_position[0] > window_x-quantum) or snake_position[1] < 0 or snake_position[1] > window_y-quantum:
		_game_over_msg()
		return True

	# Touched the snake body
	for block in snake_body[1:]:
		if snake_position[0] == block[0] and snake_position[1] == block[1]:
			_game_over_msg()
			return True
		
	return False # No violation

def _show_updated_score(): # displaying Score function
	# creating font object score_font
	score_font = pygame.font.SysFont('times new roman', 12)
	
	# create the display surface object 
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, (255,255,255))
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

# -------- Executable code ---------
	
run_game(0,10)