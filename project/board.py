
class Board:

    GUIBOARD_LEFT = 40  # in px
    GUIBOARD_UP = 40    # in px

    # Board State
    FINISHED = 0
    # End Board State

    board_id = None # string, format: 'row-column'
    board_data = None
    board_player = None
    board_piece = None
    board_state = None

    def __init__():
        pass

    def break_id(): # no idea for the function name
        tmp = Board.board_id.split('-')
        return [int(tmp[0]), int(tmp[1])]

    def get_id():
        return Board.board_id

    def get_board_player():
        return Board.board_player
    
    def set_board_player(playerA, playerB):
        if Board.board_player == None: # prevent used board to be overwritten
            Board.board_player = (playerA, playerB)
        
    def get_board_piece():
        return Board.board_piece
    
    def set_board_piece(pieceA, colorA, pieceB, colorB):
        # need board ID check to assign color
        Board.board_piece = [[pieceA, colorA], [pieceB, colorB]]

    def get_board_data():
        return Board.board_data

    def get_board_state():
        return Board.board_state

    def set_board_state(state):
        Board.board_state = state

    def position_to_pixel(coordinate):
        pass

    def position_to_coordinate(pixel):
        pass