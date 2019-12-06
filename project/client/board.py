
class Board:

    # Board State
    FINISHED = 0
    # End Board State

    board_id = None # string, format: 'row-column'
    board_data = None
    board_player = None
    board_piece = None
    board_state = None

    def __init__(self, board_data):
        self.board_data = board_data
        # Debug only, should be set from gameserver
        self.board_id = 0
        #
        pass

    def break_id(self): # no idea for the function name
        tmp = self.board_id.split('-')
        return [int(tmp[0]), int(tmp[1])]

    def is_valid(self, coordinate): # may be moved to game server with addition board/board_id parameter
        colrow = self.break_id()
        if abs(colrow[0] - coordinate[0]) <= 1 and abs(colrow[1] - coordinate[1]) <= 1 and self.board_data[coordinate[1]-1][coordinate[0]-1] == '-': # need to check outside writable region
            return True
        return False

    def get_id(self):
        return self.board_id

    def get_board_player(self):
        return self.board_player
    
    def set_board_player(self, playerA, playerB):
        if self.board_player == None: # prevent used board to be overwritten
            self.board_player = (playerA, playerB)
        
    def get_board_piece(self):
        return self.board_piece
    
    def set_board_piece(self, pieceA, pieceB):
        self.board_piece = [pieceA, pieceB]

    def get_board_data(self):
        return self.board_data

    def get_board_state(self):
        return self.board_state

    def set_board_state(self, state):
        self.board_state = state
