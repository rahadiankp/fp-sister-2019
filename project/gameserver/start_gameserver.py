# from project.gameserver.tttserver import TicTacToeServer
import Pyro4
import tttserver


def start_server(host: str, proxy_uri_list: list):
    daemon = Pyro4.Daemon(host=host)
    tictactoe_server = tttserver.TicTacToeServer(proxy_uri_list)
    uri = daemon.register(tictactoe_server)
    tictactoe_server.server_own_uri = uri
    print("Game Server is running on URI:")
    print(tictactoe_server.server_own_uri)
    tictactoe_server.register_to_rm()
    tictactoe_server.connect_to_tm()

    daemon.requestLoop()


if __name__ == "__main__":
    proxy_list = [
        "PYRONAME:proxyserver-1@localhost:8888",
        "PYRONAME:proxyserver-2@localhost:8888",
        "PYRONAME:proxyserver-3@localhost:8888"
    ]
    start_server("localhost", proxy_list)