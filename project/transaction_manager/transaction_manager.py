import getopt
import sys

import Pyro4

from project.transaction_manager.transaction_manager_api import TransactionManagerApi


class TransactionManager:

    def __init__(self, name, host, port):
        self.host = host
        self.port = port
        self.name = name

    def start(self):
        daemon = Pyro4.Daemon(host=self.host)
        ns = Pyro4.locateNS(self.host, self.port)
        api = Pyro4.expose(TransactionManagerApi)
        uri_tm = daemon.register(api)
        ns.register("{}" . format(self.name), uri_tm)
        print(uri_tm)
        daemon.requestLoop()


if __name__ == '__main__':
    NAME = ""
    HOST = ""
    PORT = 0

    options, misc = getopt.getopt(sys.argv[1:], "n:h:p:",
                                  ["name=", "host=", "port="])
    for opt, val in options:
        if opt in ["-n", "--name"]:
            NAME = val
        elif opt in ["-h", "--host"]:
            HOST = val
        elif opt in ["-p", "--port"]:
            PORT = int(val)
        TransactionManager(NAME, HOST, PORT).start()

