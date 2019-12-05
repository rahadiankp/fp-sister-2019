from project.gameserver.boardserver import Board
import Pyro4


@Pyro4.behavior(instance_mode="single")
class TicTacToeServer(object):
    WINPOS = [
        ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),  # HORIZONTAL
        ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),  # VERTICAL
        ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)),  # DIAGONAL
    ]
    PIECES = ['X', 'O']

    def __init__(self, rm_proxy_uri):
        self.board_list = [Board(i, TicTacToeServer.PIECES, TicTacToeServer.WINPOS) for i in range(6)]
        self.rm_proxy = TicTacToeServer.rm_proxy_uri(rm_proxy_uri)
        self.tm_proxy = TicTacToeServer.connect_to_proxy(self.rm_proxy.get_transaction_manager_uri())
        self.server_own_uri = ""

    @staticmethod
    def connect_to_proxy(uri: str):
        proxy = Pyro4.Proxy(uri)

        return proxy

    def handle_start(self, username):
        for i, board in enumerate(self.board_list):
            is_available, player_id = board.register_player(username)

            if is_available:
                return {
                    'status': 'OK',
                    'board_id': i,
                    'player_id': player_id
                }

        return {
            'status': 'FAIL',
            'message': 'No board available'
        }

    def handle_put(self, board_id, username, x, y):
        self.board_list[board_id].make_move(username, x, y)
        return {
            'status': 'OK'
        }

    def handle_check(self, board_id, username):
        return {
            'status': 'OK',
            'data': self.board_list[board_id].check_player_status(username)
        }

    @Pyro4.expose
    def push_command(self, command_data):
        action = command_data['action']
        board_id = command_data.get('board_id')
        username = command_data.get('username')

        if action == 'START':
            return self.handle_start(username)

        elif action == 'PUT':
            return self.handle_put(board_id, username, command_data['x'], command_data['y'])

        elif action == 'CHECK':
            return self.handle_check(board_id, username)

        elif action == 'UPDATE':
            pass

    def get_all_boards_state(self):
        board_states = []
        for board in self.board_list:
            board_states.append(board.board_data)

        return board_states

    def get_board_check(self, board_id, player_name) -> str:
        board = self.board_list[board_id]
        return board.check_player_status(player_name)
