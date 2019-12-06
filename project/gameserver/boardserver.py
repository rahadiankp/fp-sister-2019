class Board(object):

    def __init__(self, id: int, pieces: list, winpos_list: list):
        self.id = id
        self.pieces = pieces  # ['X', '0'], injection
        self.winpos_list = winpos_list
        self.game_started = False
        self.game_end_message = None  # "WIN 0" -> player 1 wins, "WIN 1" -> player 2 wins
        self.player_name_list = []  # 0 -> X, 1 -> O
        self.is_player_1_turn = 0
        self.board_data = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ]

    def reset_board(self):
        self.game_started = False
        self.game_end_message = None
        self.player_name_list = []
        self.is_player_1_turn = 0
        self.board_data = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ]

    def check_status(self, player_name):
        player_index = -1
        try:
            player_index = self.player_name_list.index(player_name)
        except ValueError:
            return False, -1, "NPLYR"  # not registered player

        # check if game not started yet
        if not self.game_started:
            return False, player_index, "NST"  # not started

        # check if victory has been achieved
        if self.game_end_message:
            game_end_message = self.game_end_message
            self.reset_board()
            return False, player_index, game_end_message

        player_turn = bool(player_index)
        if player_turn != self.is_player_1_turn:
            return False, player_index, "NTRN"

        return True, player_index, "TURN"

    def register_player(self, player_name):
        # if board full
        if len(self.player_name_list) >= 2:
            return False, -1

        # if identic username found
        if player_name in self.player_name_list:
            return False, -1

        self.player_name_list.append(player_name)
        if len(self.player_name_list) == 2:
            self.game_started = True

        return True, len(self.player_name_list) - 1

    def switch_turn(self):
        self.is_player_1_turn = not self.is_player_1_turn

    def check_winning(self):
        for ((x1, y1), (x2, y2), (x3, y3)) in self.winpos_list:
            a = self.board_data[y1][x1]
            b = self.board_data[y2][x2]
            c = self.board_data[y3][x3]
            if a == '-' or b == '-' or c == '-':
                continue
            if self.board_data[y1][x1] == self.board_data[y2][x2] == self.board_data[y3][x3]:
                piece_winning = self.board_data[y1][x1]
                piece_index = self.pieces.index(piece_winning)
                self.game_end_message = "WIN {0}".format(piece_index)
                return True, self.game_end_message

        return False, "NOWIN"

    def check_player_status(self, player_name) -> str:
        return self.check_status(player_name)[2]

    @staticmethod
    def valid_coordinate(x, y):
        if 0 > x > 2 or 0 > y > 2:
            return False
        return True

    def make_move(self, player_name, x: int, y: int) -> str:
        print('sukses3')
        status, player_index, msg = self.check_status(player_name)
        print('sukses4')
        if not status:
            return msg

        # check if coord has piece already
        if self.board_data[y][x] != "-" or not Board.valid_coordinate(x, y):
            return "BAD"
        print('sukses4')
        piece = self.pieces[player_index]
        print('sukses5')
        self.board_data[y][x] = piece
        print('sukses6')

        self.switch_turn()
        print('sukses7')

        # immediately send winning msg to winning player after the move
        status, msg = self.check_winning()
        if status:
            return msg
        print('sukses8')

        return "OK {0} {1},{2}".format(piece, x, y)