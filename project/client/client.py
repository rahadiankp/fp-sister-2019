import Pyro4
from project.client.board import Board
from project.client.drawer import Drawer


class Client:
    
    board = None
    drawer = None

    def __init__(self, username, proxy_uri):
        # this client's player piece ('o' or 'x') used as parameter below
        self.username = username
        self.proxy = Pyro4.Proxy(proxy_uri)
        register_response: dict = self.proxy.push_command("START " + username)
        if register_response['status'] != "OK":
            raise Exception(register_response['message'])
        self.board_id = register_response['board_id']
        self.player_id = register_response['player_id']
        latest_board: dict = self.proxy.push_command("UPDATE")
        print(latest_board)
        self.board = Board(latest_board['data'])
        self.drawer = Drawer(self.board, self.username, str(self.board_id), self.player_id, self.proxy)

    def start(self):
        self.drawer.update_screen()


if __name__ == "__main__":
    client = Client("asd", "PYRONAME:proxyserver@localhost:8888")
    client.start()