import pygame
import time
import sys

import pprint

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
    my_piece = None
    drawn = None
    # end of pygame variable

    def __init__(self, board, piece):
        self.board = board
        # need self.drawn initialization here
        self.drawn = self.init_drawn()
        self.my_piece = piece
        self.load_resource()
        self.init_pygame(self.board)

    def update_screen(self):
        running = True
        mousepx = None
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousepx = pygame.mouse.get_pos()
                        print(mousepx, self.position_to_coordinate(mousepx), self.position_to_pixel(self.position_to_coordinate(mousepx)))
                        self.place_piece(mousepx)

                    self.draw_board()
                    self.draw_piece(self.board.get_board_data())
                    pygame.display.update()
        except KeyboardInterrupt:
            sys.exit()

    def load_resource(self):
        self.resource = {}
        
        # load all resource here
        self.resource.update({'board': pygame.image.load('assets/board.png')})
        self.resource.update({'o': pygame.image.load('assets/red_o.png')})
        self.resource.update({'x': pygame.image.load('assets/blue_x.png')})

    def draw(self, board): # will be threaded
        self.draw_board()
        self.draw_piece(board.board_data)
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
        col = x // Drawer.GUIBOARD_RECTSIZE + 1
        row = y // Drawer.GUIBOARD_RECTSIZE + 1

        return [col, row]
    
    def place_piece(self, pixel):
        coordinate = self.position_to_coordinate(pixel)
        if not self.board.is_valid(coordinate):
            # not valid move response here
            print('Invalid move')
            return
        # generate command string here (to be saved to TM)
        cmd = 'PUT {} to ({},{}) ID {}'.format(self.my_piece, str(coordinate[0]), str(coordinate[1]), self.board.get_id())
        self.board.board_data[coordinate[1]-1][coordinate[0]-1] = self.my_piece
        pprint.pprint(self.board.get_board_data())

    # set pygame config
    def init_pygame(self, board):
        pygame.init()
        pygame.display.set_caption(self.CAPTION)
        self.screen = pygame.display.set_mode(self.RESOLUTION)
                
    def init_drawn(self):
        self.drawn = self.board.get_board_data()
        for row in range(0, 9):
            for column in range(0, 9):
                pix = self.position_to_pixel([column, row])
                if self.drawn[row][column] == '-':
                    self.drawn[row][column] = [None, pix]
                elif self.drawn[row][column] == 'x':
                    self.drawn[row][column] = [self.resource['x'].image.copy(), pix]
                elif self.drawn[row][column] == 'o':
                    self.drawn[row][column] = [self.resource['o'].image.copy(), pix]