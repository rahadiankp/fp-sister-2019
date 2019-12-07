from project.gameserver.boardserver import Board
import Pyro4
import Pyro4.errors


@Pyro4.behavior(instance_mode="single")
class TicTacToeServer(object):
    WINPOS = [
        ((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),  # HORIZONTAL
        ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),  # VERTICAL
        ((0, 0), (1, 1), (2, 2)), ((2, 0), (1, 1), (0, 2)),  # DIAGONAL
    ]
    PIECES = ['X', 'O']

    def __init__(self, proxy_uri_list: list):
        self.board_list = [Board(i, TicTacToeServer.PIECES, TicTacToeServer.WINPOS) for i in range(6)]
        self.player_board_map = {}
        self.rm_proxy_list = [TicTacToeServer.connect_to_proxy(proxy_uri) for proxy_uri in proxy_uri_list]
        self.tm_proxy = None
        self.server_own_uri = ""
        self.is_ready = False

    @staticmethod
    def connect_to_proxy(uri: str):
        proxy = Pyro4.Proxy(uri)

        return proxy

    def connect_to_tm(self):
        # agree to only 1 tm uri
        tm_uri = self.rm_proxy_list[0].get_transaction_manager_uri()
        for i in range(1, len(self.rm_proxy_list)):
            tm_uri_temp = self.rm_proxy_list[i].get_transaction_manager_uri()
            if tm_uri != tm_uri_temp:
                raise Exception("Transaction Manager URI not matched")

        for proxy in self.rm_proxy_list:
            tm_uri = proxy.get_transaction_manager_uri()
            try:
                print(tm_uri)
                self.tm_proxy = TicTacToeServer.connect_to_proxy(tm_uri)
                break
            except Pyro4.errors.CommunicationError:
                continue

        if not self.tm_proxy:
            raise Exception("No available Transaction Manager proxy connected")

        up_to_date = False
        self.is_ready = False
        from_index = 0
        commands = self.tm_proxy.get_data_to_last_from(from_index)
        latest_len = len(commands)

        while not up_to_date:
            for command in commands:
                self.push_command(command, True)

            new_latest_len = self.tm_proxy.get_data_length()
            up_to_date = new_latest_len == latest_len
            from_index = latest_len - 1
            latest_len = new_latest_len
            if not up_to_date:
                commands = self.tm_proxy.get_data_to_last_from(from_index)

        self.is_ready = True

    def register_to_rm(self):
        for proxy in self.rm_proxy_list:
            proxy.register_server(self.server_own_uri)

    @Pyro4.expose
    def get_uri(self):
        return self.server_own_uri

    @Pyro4.expose
    def push_command(self, command_data, is_fail_over=False):
        # print(command_data)
        if not self.is_ready and not is_fail_over:
            return {
                'status': 'NOT_READY'
            }
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
            return self.handle_update()
        elif action == "UNREGISTER":
            return self.handle_unregister(board_id, username)
        elif action == "RPOL":
            return self.handle_reset_poll(board_id, username)
        else:
            return {
                'status': 'FAILED',
                'message': 'Unknown command'
        }

    def handle_start(self, username):
        if username in self.player_board_map:
            board_id, player_id = self.player_board_map[username]
            return {
                'status': 'OK',
                'message': 'Resuming game',
                'board_id': board_id,
                'player_id': player_id
            }
        for i, board in enumerate(self.board_list):
            is_available, player_id = board.register_player(username)

            if is_available:
                self.player_board_map[username] = (i, player_id)
                return {
                    'status': 'OK',
                    'board_id': i,
                    'player_id': player_id
                }

        return {
            'status': 'FAILED',
            'message': 'No board available'
        }

    def handle_put(self, board_id, username, x, y):
        if board_id >= 6:
            return {
                'status': 'FAILED',
                'message': 'Invalid board id'
            }
        ok_response = ["OK", "DRAW", "WIN"]
        put_response = self.board_list[board_id].make_move(username, x, y)
        if put_response.split()[0] in ok_response:
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
            return {
                'status': 'FAILED',
                'message': 'Invalid board id'
            }
        return {
            'status': 'OK',
            'message': self.board_list[board_id].check_player_status(username)
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

    def handle_unregister(self, board_id, username):
        if board_id >= 6:
            return {
                'status': 'FAILED',
                'message': 'Invalid board id'
            }

        # board = self.board_list[board_id]
        try:
            # board.player_name_list.remove(username)
            self.player_board_map.pop(username)
            return {
                'status': 'OK',
                'message': 'Username ' + username + " removed from board " + str(board_id)
            }
        except ValueError:
            return {
                'status': 'FAILED',
                'message': 'Username ' + username + " not in board " + str(board_id)
            }

    def handle_reset_poll(self, board_id, username):
        if board_id >= 6:
            return {
                'status': 'FAILED',
                'message': 'Invalid board id'
            }

        board = self.board_list[board_id]
        reset_poll_response = board.reset_board_poll(username)
        if reset_poll_response.split()[0] == "OK":
            return {
                'status': 'OK',
                'message': reset_poll_response
            }

        return {
            'status': 'FAILED',
            'message': reset_poll_response
        }

    @Pyro4.expose
    def ping(self):
        return "PONG"

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