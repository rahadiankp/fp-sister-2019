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
        self.rm_proxy = TicTacToeServer.connect_to_proxy(rm_proxy_uri)
        self.tm_proxy = None
        self.server_own_uri = ""

    @staticmethod
    def connect_to_proxy(uri: str):
        proxy = Pyro4.Proxy(uri)

        return proxy

    def connect_to_tm(self):
        self.tm_proxy = TicTacToeServer.connect_to_proxy(self.rm_proxy.get_transaction_manager_uri())

    def register_to_rm(self):
        self.rm_proxy.register_server(self.server_own_uri)

    @Pyro4.expose
    def get_uri(self):
        return self.server_own_uri

    @Pyro4.expose
    def push_command(self, command_data):
        action = command_data['action']
        board_id = command_data.get('board_id')
        username = command_data.get('username')
        print('sukses2')
        if action == 'START':
            return self.handle_start(username)
        elif action == 'PUT':
            return self.handle_put(board_id, username, command_data['x'], command_data['y'])
        elif action == 'CHECK':
            return self.handle_check(board_id, username)
        elif action == 'UPDATE':
            return self.handle_update()
        else:
            return {
                'status': 'FAIL',
                'message': 'Unknown command'
        }

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
        put_response = self.board_list[board_id].make_move(username, x, y)
        if put_response.split()[0] == 'OK':
            return {
                'status': 'OK',
                'message': put_response
            }

        return {
                'status': 'FAILED',
                'message': put_response
        }

    def handle_check(self, board_id, username):
        if board_id >= 6:
            return {}
        return {
            'status': 'OK',
            'data': self.board_list[board_id].check_player_status(username)
        }

    def handle_update(self) -> dict:
        board_states = [[] for i in range(6)]

        for i in range(2):
            board1 = self.board_list[3*i]
            board2 = self.board_list[3*i+1]
            board3 = self.board_list[3*i+2]
            board_states[3*i] = board1.board_data[0] + board2.board_data[0] + board3.board_data[0]
            board_states[3*i+1] = board1.board_data[1] + board2.board_data[1] + board3.board_data[1]
            board_states[3*i+2] = board1.board_data[2] + board2.board_data[2] + board3.board_data[2]

        return {'status': 'OK', 'data': board_states}

    """Debug methods
    
    """

    @Pyro4.expose
    def verbose_server(self):
        result = []
        for board in self.board_list:
            a = dict()
            a["player_1"] = board.player_name_list[0] if len(board.player_name_list) > 0 else None
            a["player_2"] = board.player_name_list[1] if len(board.player_name_list) > 1 else None
            a["board_data"] = board.board_data
            result.append(a)

        return result