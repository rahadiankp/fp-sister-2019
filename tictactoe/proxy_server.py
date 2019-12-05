from tictactoe.proxy import Proxy
import Pyro4


def start_sever(host="localhost"):
    daemon = Pyro4.Daemon(host=host)
    proxy = Proxy("wkwk")
    uri = daemon.register(proxy)

    print(uri)
    daemon.requestLoop()


if __name__ == "__main__":
    start_sever()