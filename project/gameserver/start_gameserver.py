from project.gameserver.tttserver import TicTacToeServer
import Pyro4


def start_server(host: str, rm_proxy_uri):
    daemon = Pyro4.Daemon(host=host)
    tictactoe_server = TicTacToeServer(rm_proxy_uri)
    uri = daemon.register(tictactoe_server)
    tictactoe_server.server_own_uri = uri
    print("Game Server is running on URI:")
    print(tictactoe_server.server_own_uri)
    tictactoe_server.register_to_rm()
    tictactoe_server.connect_to_tm()

    daemon.requestLoop()


if __name__ == "__main__":
    start_server("localhost", "PYRONAME:proxyserver@localhost:8888")