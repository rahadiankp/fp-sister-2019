# from project.transaction_manager.transaction_manager_api import TransactionManagerApi
import getopt
import sys
import Pyro4
import transaction_manager_api


class TransactionManager:

    def __init__(self, name, host, port, bootstrap, proxy_uri_list):
        self.host = host
        self.port = port
        self.name = name
        self.bootstrap = bootstrap
        self.proxy_uri_list = proxy_uri_list

    def start(self):
        daemon = Pyro4.Daemon(host=self.host)
        ns = Pyro4.locateNS(self.host, self.port)
        # api = Pyro4.expose(transaction_manager_api.TransactionManagerApi)
        api = transaction_manager_api.TransactionManagerApi(
            "PYRONAME:" + self.name + "@" + self.host + ":" + str(self.port),
            self.proxy_uri_list,
            self.bootstrap
        )
        uri_tm = daemon.register(api)
        ns.register("{}" . format(self.name), uri_tm)
        print(uri_tm)
        daemon.requestLoop()


if __name__ == '__main__':
    NAME = ""
    HOST = ""
    PORT = 0
    BOOTSTRAP = False

    options, misc = getopt.getopt(sys.argv[1:], "n:h:p:b",
                                  ["name=", "host=", "port=", "bootstrap"])
    for opt, val in options:
        if opt in ["-n", "--name"]:
            NAME = val
        elif opt in ["-h", "--host"]:
            HOST = val
        elif opt in ["-p", "--port"]:
            PORT = int(val)
        elif opt in ["-b", "--bootstrap"]:
            BOOTSTRAP = True
    proxy_list = [
        "PYRONAME:proxyserver-1@localhost:8888",
        "PYRONAME:proxyserver-2@localhost:8888",
        "PYRONAME:proxyserver-3@localhost:8888"
    ]
    TransactionManager(NAME, HOST, PORT, BOOTSTRAP, proxy_list).start()

