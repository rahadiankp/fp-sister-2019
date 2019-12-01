import pygame

class Drawer:

    GUIBOARD_LEFT = 40  # in px
    GUIBOARD_UP = 40    # in px

    GUIBOARD_RECTSIZE = 80  # in px
    GUIBOARD_OFFSET = 2     # in px

    Board = None

    def __init__(self):
        pass

    def draw(self, board):
        Drawer.draw_board()
        Drawer.draw_piece(board.board_data)
        # create function for every feature to be drawn

    def draw_board(self): # draw visualization of board without piece
        pass

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