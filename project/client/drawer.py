import pygame
import time
import sys

class Drawer:

    GUIBOARD_LEFT = 40  # in px
    GUIBOARD_UP = 40    # in px

    GUIBOARD_RECTSIZE = 80  # in px
    GUIBOARD_OFFSET = 2     # in px

    board = None
    is_turn = False

    # pygame
    # pygame config, used for game setting
    CAPTION = "Game Board"
    RESOLUTION = (800, 560)
    # end of game setting
    # pygame variable
    screen = None
    resource = None
    # end of pygame variable

    def __init__(self, board):
        self.board = board
        self.load_resource()
        self.init_pygame(self.board)

    def debug_run(self):
        # debug only
        running = True
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    self.draw_board()
                    pygame.display.update()
        except KeyboardInterrupt:
            sys.exit()

    def load_resource(self):
        self.resource = {}
        
        # load all resource here
        self.resource.update({'board': pygame.image.load('assets/board.png')})
        # self.resource.update({'red_o': pygame.image.load('assets/red_o.png')})
        # self.resource.update({'red_x': pygame.image.load('assets/red_x.png')})
        # self.resource.update({'blue_o': pygame.image.load('assets/blue_o.png')})
        # self.resource.update({'blue_x': pygame.image.load('assets/blue_x.png')})

    def draw(self, board): # will be threaded
        Drawer.draw_board()
        Drawer.draw_piece(board.board_data)
        # create function for every feature to be drawn

    def draw_board(self): # draw visualization of board without piece
        self.screen.blit(self.resource['board'], (0, 0))

    def draw_piece(self, board_data): # draw board's piece
        pass

    def get_pivot_pixel(self, pixel): # get pivot pixel (upper left) of board's rectangle
        x = ( (pixel[0] - Drawer.GUIBOARD_LEFT) // Drawer.GUIBOARD_RECTSIZE ) * Drawer.GUIBOARD_RECTSIZE
        y = ( (pixel[1] - Drawer.GUIBOARD_UP) // Drawer.GUIBOARD_RECTSIZE ) * Drawer.GUIBOARD_RECTSIZE

        return [x, y]

    def position_to_pixel(self, coordinate):
        col = coordinate[0] - 1
        row = coordinate[1] - 1
        x = Drawer.GUIBOARD_LEFT + Drawer.GUIBOARD_RECTSIZE * col + Drawer.GUIBOARD_OFFSET
        y = Drawer.GUIBOARD_UP + Drawer.GUIBOARD_RECTSIZE * row + Drawer.GUIBOARD_OFFSET

        return [x, y]

    def position_to_coordinate(self, pixel):
        x = pixel[0] - Drawer.GUIBOARD_LEFT
        y = pixel[1] - Drawer.GUIBOARD_UP
        col = x / Drawer.GUIBOARD_RECTSIZE
        row = y / Drawer.GUIBOARD_RECTSIZE

        return [row, col]
    
    # set pygame config
    def init_pygame(self, board):
        pygame.init()
        pygame.display.set_caption(self.CAPTION)
        self.screen = pygame.display.set_mode(self.RESOLUTION)
                
        