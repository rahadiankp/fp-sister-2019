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

    @staticmethod
    def connect_to_proxy(uri: str):
        proxy = Pyro4.Proxy(uri)

        return proxy

    @Pyro4.expose
    def push_command(self, command):
        '''Return msg to client

        Command list & responses:
        - START <player_name>
            SUCCESS:
                -> OK <board_id> : Successfully registered to board <board_id>
            FAILED:
                -> FULL : Failed to register/start a game due to maximum player count reached
        - PUT <player_name> <board_id> <coordinate>
            SUCCESS:
                -> OK
        '''
