# from project.client.board import Board
# from project.client.drawer import Drawer
import getopt
import sys
import Pyro4
import board
import drawer
import start_scene


class Client:
    
    board = None
    drawer = None

    def __init__(self, username, proxy_uri, spectator_mode=False):
        self.username = username
        try:
            self.proxy = Pyro4.Proxy(proxy_uri)
        except:
            print("Invalid URI")
            return
        if not spectator_mode:
            register_response: dict = self.proxy.push_command("START " + username)
            if register_response['status'] != "OK":
                raise Exception(register_response['message'])
            self.board_id = register_response['board_id']
            self.player_id = register_response['player_id']
        else:
            self.board_id = "X"
            self.player_id = "X"

        latest_board: dict = self.proxy.push_command("UPDATE")
        self.board = board.Board(latest_board['data'])
        self.drawer = drawer.Drawer(self.board, self.username, str(self.board_id),
                                    self.player_id, self.proxy, spectator_mode)

    def start(self):
        self.drawer.update_screen()


if __name__ == "__main__":
    USERNAME = ""
    PROXY_URI = ""
    SPECTATOR = False

    main_screen = start_scene.StartScene()
    main_screen.start_scene()
    username = main_screen.get_username()
    uri = "PYRONAME:proxyserver-3@localhost:8888"

    options, misc = getopt.getopt(sys.argv[1:], "u:h:s",
                                  ["username=", "host=", "spectator"])
    for opt, val in options:
        if opt in ["-u", "--username"]:
            USERNAME = val
        elif opt in ["-h", "--host"]:
            PROXY_URI = val
        elif opt in ["-s", "--spectator"]:
            SPECTATOR = True
        elif opt in ["-s", "--spectator"]:
            SPECTATOR = True
    client = Client(USERNAME, PROXY_URI, SPECTATOR)
    # client = Client("receh", "PYRONAME:proxyserver-3@localhost:8888")
    # client = Client("alcredo", "PYRONAME:proxyserver-1@localhost:8888")
    # client = Client("teje", "PYRONAME:proxyserver-2@localhost:8888")
    # client = Client("alfian", "PYRONAME:proxyserver-1@localhost:8888")
    client.start()