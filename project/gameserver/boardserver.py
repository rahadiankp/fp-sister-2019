class Board(object):

    def __init__(self, id: int, pieces: list, winpos_list: list):
        self.id = id
        self.pieces = pieces  # ['X', '0'], injection
        self.winpos_list = winpos_list
        self.game_started = False
        self.game_end_message = None  # "WIN 0" -> player 1 wins, "WIN 1" -> player 2 wins
        self.player_name_list = []  # 0 -> X, 1 -> O
        self.is_player_1_turn = True
        self.board_data = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ]

    def reset_board(self):
        self.game_started = False
        self.player_name_list = []
        self.is_player_1_turn = 0
        self.board_data = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ]

    def check_player_status(self, player_name):
        player_index = -1
        try:
            player_index = self.player_name_list.index(player_name)
        except ValueError:
            return False, -1, "NPLYR"  # not registered player

        # check if game not started yet
        if not self.game_started:
            return False, player_index, "NST"  # not started

        # check if victory has been achieved
        if not self.game_end_message:
            return False, player_index, self.game_end_message

        player_turn = not bool(player_index)
        if player_turn != self.is_player_1_turn:
            return False, player_index, "NTRN"

        return True, player_index, "TURN"

    def register_player(self, player_name):
        if len(self.player_name_list) > 2:
            return False

        self.player_name_list.append(player_name)
        if len(self.player_name_list) == 2:
            self.game_started = True

        return True

    def switch_turn(self):
        self.is_player_1_turn = not self.is_player_1_turn

    def make_move(self, player_name, x, y) -> str:
        status, player_index, msg = self.check_player_status(player_name)
        if not status:
            return msg

        # check if coord has piece already
        if self.board_data[y][x] != "-":
            return False

        piece = self.pieces[player_index]
        self.board_data[y][x] = piece

        self.switch_turn()

        return True
