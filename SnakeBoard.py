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

    G_SPD = 3 # game speed up to 10fps

    # Window size (always a multiple of 10)
    WRES = 4
    G_WIDTH = 16 * WRES
    G_HEIGHT = 16 * WRES
    S_WIDTH = 1920
    S_HEIGHT = 1080
    BORDER=1
#endregion

#region ----- Methods -----

    def __init__(self, num_games):
        print("SnakeBoard instance created.")
        self.num_games = num_games

    def init_board(self):    
        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()      
        
        # Initializing pygame window in correct position
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        pygame.init()

        # Initialize game window
        pygame.display.set_caption('Snake Game')
        self._calc_boardsize()
        self.game_window = pygame.display.set_mode((self.ncols*(SnakeBoard.G_WIDTH + 2*SnakeBoard.BORDER), self.nrows*(SnakeBoard.G_HEIGHT+2*SnakeBoard.BORDER) ))

    def quit_board(self):
        pygame.quit()

    def clear_board(self):
        # Clear game board
        self.game_window.fill(SnakeBoard.BLACK) 

    def update_board_elements(self, s_games):
        for num_game, game in enumerate(s_games):
            [ox,oy]= self._calc_gamepos(num_game)
            
            # Draw border
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(0+ox, 0+oy, SnakeBoard.BORDER, SnakeBoard.G_WIDTH+2*SnakeBoard.BORDER))
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(SnakeBoard.G_HEIGHT+SnakeBoard.BORDER+ox,0+oy, SnakeBoard.BORDER, SnakeBoard.G_WIDTH+2*SnakeBoard.BORDER))
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(0+ox, 0+oy, SnakeBoard.G_HEIGHT+2*SnakeBoard.BORDER,SnakeBoard.BORDER ))
            pygame.draw.rect(self.game_window, SnakeBoard.YELLOW, pygame.Rect(0+ox, SnakeBoard.G_WIDTH + SnakeBoard.BORDER+oy,  SnakeBoard.G_HEIGHT+ 2*SnakeBoard.BORDER, SnakeBoard.BORDER))
            
            # Draw snake
            for pos in game.body_snake: 
                # Don't draw out of the board
                pos[0] = 0 if pos[0] < 0 else pos[0] 
                pos[0] = SnakeBoard.G_WIDTH - SnakeBoard.WRES if pos[0] > SnakeBoard.G_WIDTH - SnakeBoard.WRES else pos[0] 
                pos[1] = 0 if pos[1] < 0 else pos[1] 
                pos[1] = SnakeBoard.G_HEIGHT - SnakeBoard.WRES if pos[1] > SnakeBoard.G_HEIGHT - SnakeBoard.WRES else pos[1] 

                scolor = SnakeBoard.RED if game.game_over == True else SnakeBoard.GREEN
                pygame.draw.rect(self.game_window, scolor, pygame.Rect(pos[0]+ SnakeBoard.BORDER + ox, pos[1]+ SnakeBoard.BORDER + oy, SnakeBoard.WRES, SnakeBoard.WRES))
            
            # Draw food
            scolor = SnakeBoard.GRAY if game.game_over == True else SnakeBoard.WHITE
            pygame.draw.rect(self.game_window, scolor, pygame.Rect(game.pos_food[0]+ SnakeBoard.BORDER+ox, game.pos_food[1]+ SnakeBoard.BORDER+oy, SnakeBoard.WRES, SnakeBoard.WRES))
            
        # Refresh game screen
        pygame.display.update()

        # Frame Per Second / Refresh Rate
        self.fps.tick(SnakeBoard.G_SPD)

    def _calc_boardsize(self):
        self.ncols = int(np.ceil(np.sqrt(self.num_games)))
        self.nrows = int(np.round(np.sqrt(self.num_games)))



    def _calc_gamepos(self, num_game):
        n=0        
        for x in range(self.ncols):
            for y in range(self.nrows):
                if num_game==n:
                    game_x= x * (SnakeBoard.G_WIDTH + SnakeBoard.BORDER)
                    game_y= y * (SnakeBoard.G_HEIGHT + SnakeBoard.BORDER)
                    return [game_x, game_y]
                
                n=n+1
        
        return -1

    #endregion