import Pyro4

from project.transaction_manager.transaction_manager_api import TransactionManagerApi


class TransactionManager:

    def start(self):
        daemon = Pyro4.Daemon(host="localhost")
        ns = Pyro4.locateNS("localhost",8888)
        api = Pyro4.expose(TransactionManagerApi)
        uri_tm = daemon.register(api)
        ns.register("{}" . format("transaction-manager"), uri_tm)
        print(uri_tm)
        daemon.requestLoop()


if __name__ == '__main__':
    TransactionManager().start()
