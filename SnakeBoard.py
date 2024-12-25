# importing libraries
import pygame
import os
import numpy as np

class SnakeBoard:

#region ----- Class variables -----
    # defining colors
    BLACK = pygame.Color(0, 0, 0)
    GRAY = pygame.Color(50, 50, 50)
    WHITE = pygame.Color(255, 255, 255)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    YELLOW = pygame.Color(255, 255,0)

    G_SPD = 100 # game speed up to 10fps

    # Window size
    WRES = 5
    G_WIDTH = 6
    G_HEIGHT = G_WIDTH # Keep same as G_WIDTH - must be square!
    S_WIDTH = 1024
    S_HEIGHT = 768
    BORDER = 1

    W_WIDTH = G_WIDTH * WRES
    W_HEIGHT = G_HEIGHT * WRES
#endregion

#region ----- Methods -----

    def __init__(self, num_games, visuals=True):
        print("SnakeBoard instance created.")
        self.num_games = num_games
        self.visuals = visuals

    def init_board(self):    
        if self.visuals:
            # FPS (frames per second) controller
            self.fps = pygame.time.Clock()  
            
            # Initializing pygame window in correct position
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2,2)
            pygame.init()

            # Initialize game window
            pygame.display.set_caption('Snake Game')
            self._calc_boardsize_screen()
            self.game_window = pygame.display.set_mode((self.ncols*(SnakeBoard.W_WIDTH + 2*SnakeBoard.BORDER), self.nrows*(SnakeBoard.W_HEIGHT+2*SnakeBoard.BORDER) ))

    def quit_board(self):
        if self.visuals:
            pygame.quit()

    def clear_board(self):
        if self.visuals:
            # Clear game board
            self.game_window.fill(SnakeBoard.BLACK) 

    def update_board_elements(self, s_games):
        if self.visuals == False:
            return 
        
        for num_game, game in enumerate(s_games):
            [ox,oy]= self._calc_gamepos_screen(num_game)
            
            # Draw border
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(0+ox, 0+oy, SnakeBoard.BORDER, SnakeBoard.W_WIDTH+2*SnakeBoard.BORDER))
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(SnakeBoard.W_HEIGHT+SnakeBoard.BORDER+ox,0+oy, SnakeBoard.BORDER, SnakeBoard.W_WIDTH+2*SnakeBoard.BORDER))
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(0+ox, 0+oy, SnakeBoard.W_HEIGHT+2*SnakeBoard.BORDER,SnakeBoard.BORDER ))
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(0+ox, SnakeBoard.W_WIDTH + SnakeBoard.BORDER+oy,  SnakeBoard.W_HEIGHT+ 2*SnakeBoard.BORDER, SnakeBoard.BORDER))
            
            # Draw snake
            for idx, pos in enumerate(game.body_snake): 
                # Magnify according board window resolution
                pos_res = np.zeros(2)
                pos_res[0] = pos[0] * SnakeBoard.WRES
                pos_res[1] = pos[1] * SnakeBoard.WRES

                # Don't draw out of the board
                pos_res[0] = 0 if pos_res[0] < 0 else pos_res[0] 
                pos_res[0] = SnakeBoard.W_WIDTH - SnakeBoard.WRES if pos_res[0] > SnakeBoard.W_WIDTH - SnakeBoard.WRES else pos_res[0] 
                pos_res[1] = 0 if pos_res[1] < 0 else pos_res[1] 
                pos_res[1] = SnakeBoard.W_HEIGHT - SnakeBoard.WRES if pos_res[1] > SnakeBoard.W_HEIGHT - SnakeBoard.WRES else pos_res[1] 

                # Draw object
                if game.game_over == True:
                    scolor = SnakeBoard.RED  
                else:
                    r = (SnakeBoard.GREEN.r * (len(game.body_snake) - (idx+1)) +  SnakeBoard.YELLOW.r * (idx+1))/ len(game.body_snake)
                    g = (SnakeBoard.GREEN.g * (len(game.body_snake) - (idx+1)) +  SnakeBoard.YELLOW.g * (idx+1))/ len(game.body_snake)
                    b = (SnakeBoard.GREEN.b * (len(game.body_snake) - (idx+1)) +  SnakeBoard.YELLOW.b * (idx+1))/ len(game.body_snake)
                    scolor = pygame.Color(int(r),int(g),int(b),255)
                    
                pygame.draw.rect(self.game_window, scolor, pygame.Rect(pos_res[0]  + SnakeBoard.BORDER + ox, pos_res[1]  + SnakeBoard.BORDER + oy, SnakeBoard.WRES, SnakeBoard.WRES))
            
            # Draw food
            pos_food = np.zeros(2)
            pos_food[0] = game.pos_food[0] * SnakeBoard.WRES
            pos_food[1] = game.pos_food[1] * SnakeBoard.WRES
            scolor = SnakeBoard.GRAY if game.game_over == True else SnakeBoard.WHITE
            pygame.draw.rect(self.game_window, scolor, pygame.Rect(pos_food[0]+ SnakeBoard.BORDER+ox, pos_food[1]+ SnakeBoard.BORDER+oy, SnakeBoard.WRES, SnakeBoard.WRES))
            
            # Show score
            #score_font = pygame.font.SysFont('times new roman', 12)
            #score_surface = score_font.render('Score : ' + str(self.game.score), True, (255,255,255))
            #score_rect = score_surface.get_rect()
            #self.snake_board.blit(score_surface, score_rect) # displaying text

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second / Refresh Rate
        self.fps.tick(SnakeBoard.G_SPD)

    def _calc_boardsize_screen(self):
        self.ncols = int(np.ceil(np.sqrt(self.num_games)))
        self.nrows = int(np.round(np.sqrt(self.num_games)))

    def _calc_gamepos_screen(self, num_game):
        n=0        
        for x in range(self.ncols):
            for y in range(self.nrows):
                if num_game==n:
                    game_x= x * (SnakeBoard.W_WIDTH + SnakeBoard.BORDER)
                    game_y= y * (SnakeBoard.W_HEIGHT + SnakeBoard.BORDER)
                    return [game_x, game_y]
                n=n+1
        return -1

    #endregion