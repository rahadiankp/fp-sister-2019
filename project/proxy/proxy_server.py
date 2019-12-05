import Pyro4
from project.proxy.proxy_server_api import ProxyServerApi


class ProxyServer:

    def start(self):
        daemon = Pyro4.Daemon(host="localhost")
        ns = Pyro4.locateNS("localhost",8888)
        api = Pyro4.expose(ProxyServerApi)
        uri_proxy = daemon.register(api)
        ns.register("{}" . format("proxyserver"), uri_proxy)
        daemon.requestLoop()


if __name__ == '__main__':
    ProxyServer().start()
