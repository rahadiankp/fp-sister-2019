
class Board:

    # Board State
    FINISHED = 0
    # End Board State

    board_id = None # string, format: 'row-column'
    board_data = None
    board_player = None
    board_piece = None
    board_state = None

    def __init__(self):
        pass

    def break_id(self): # no idea for the function name
        tmp = Board.board_id.split('-')
        return [int(tmp[0]), int(tmp[1])]

    def is_valid(self, coordinate): # may be moved to game server with addition board/board_id parameter
        rowcol = Board.break_id()
        if abs(rowcol[0] - coordinate[0]) <= 1 and abs(rowcol[1] - coordinate[1]) <= 1:
            return True
        return False

    def get_id(self):
        return Board.board_id

    def get_board_player(self):
        return Board.board_player
    
    def set_board_player(self, playerA, playerB):
        if Board.board_player == None: # prevent used board to be overwritten
            Board.board_player = (playerA, playerB)
        
    def get_board_piece(self):
        return Board.board_piece
    
    def set_board_piece(self, pieceA, colorA, pieceB, colorB):
        # need board ID check to assign color
        Board.board_piece = [[pieceA, colorA], [pieceB, colorB]]

    def get_board_data(self):
        return Board.board_data

    def get_board_state(self):
        return Board.board_state

    def set_board_state(self, state):
        Board.board_state = state
