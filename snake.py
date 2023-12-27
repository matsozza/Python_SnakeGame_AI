# importing libraries
import pygame
import time
import random

# Main Function
def run_game():
	global change_to, direction, fruit_position, fruit_spawn, score
	_init_globals()
	while True:
		_get_key()
		_update_snake_food()
		_show_score(1, white, 'times new roman', 12)
		
		if _check_gameover() == True:
			_quit_game()
			return score

		# Refresh game screen
		pygame.display.update()

		# Frame Per Second / Refresh Rate
		fps.tick(snake_speed)

def _init_globals():
	global change_to, direction, fruit_position, fruit_spawn, score, snake_position, snake_body, game_window, black, white, red,green,blue,quantum, window_x,window_y,fps, snake_speed

	# FPS (frames per second) controller
	fps = pygame.time.Clock()
	snake_speed = 10 # game speed up to 10fps

	# Window size (always a multiple of 10)
	quantum = 5
	window_x = 30 * quantum
	window_y = 30 * quantum

	# defining colors
	black = pygame.Color(0, 0, 0)
	white = pygame.Color(255, 255, 255)
	red = pygame.Color(255, 0, 0)
	green = pygame.Color(0, 255, 0)
	blue = pygame.Color(0, 0, 255)

	# Initializing pygame
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
	global change_to, direction
	# handling key events
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				change_to = 'UP'
			if event.key == pygame.K_DOWN:
				change_to = 'DOWN'
			if event.key == pygame.K_LEFT:
				change_to = 'LEFT'
			if event.key == pygame.K_RIGHT:
				change_to = 'RIGHT'
			if event.key == pygame.K_SPACE:
				pygame.quit()
				quit()

	# Handle forbidden movements
	if change_to == 'UP' and direction != 'DOWN':
		direction = 'UP'
	if change_to == 'DOWN' and direction != 'UP':
		direction = 'DOWN'
	if change_to == 'LEFT' and direction != 'RIGHT':
		direction = 'LEFT'
	if change_to == 'RIGHT' and direction != 'LEFT':
		direction = 'RIGHT'

def _update_snake_food():
		global fruit_position, fruit_spawn, snake_body, snake_position, fruit_position, quantum, window_x, window_y, game_window, white, green, score

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
			fruit_position = [random.randrange(1, (window_x//quantum)) * quantum, random.randrange(1, (window_y//quantum)) * quantum] #create new food
		else:
			snake_body.pop() #just move snake
	
		game_window.fill(black) # clear game board
		for pos in snake_body: # draw snake
			pygame.draw.rect(game_window, green,pygame.Rect(pos[0], pos[1], quantum, quantum))
		
		# draw food
		pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], quantum, quantum))

def _check_gameover(): # check if any violation occurred
	# game over function
	def _game_over_msg():
		# creating font object my_font
		my_font = pygame.font.SysFont('times new roman', 16)
		
		# creating a text surface on which text will be drawn
		game_over_surface = my_font.render(' Your Score is : ' + str(score) + ' ', True, red, (255,255,255,100))
		
		# create a rectangular object for the text surface object
		game_over_rect = game_over_surface.get_rect()
		game_over_rect.midtop = (window_x/2, window_y/2) # setting position of the text

		# blit will draw the text on screen
		game_window.blit(game_over_surface, game_over_rect)
		pygame.display.flip()
		
		# after 2 seconds we will quit the program
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

def _show_score(choice, color, font, size): # displaying Score function
	# creating font object score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object 
	# score_surface
	score_surface = score_font.render('Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

def _quit_game():
	# deactivating pygame library
	pygame.quit()
	
	# quit the program
	#quit()

# ********** Executable code **********
print("Start")
a = run_game()
print("Final score: " + str(a))