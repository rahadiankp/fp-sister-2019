import Pyro4
from project.proxy.proxy_server_api import ProxyServerApi


def start_proxy(tm_uri):
    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS("localhost",8888)
    proxy_server_api = ProxyServerApi(tm_uri)
    uri_proxy = daemon.register(proxy_server_api)
    ns.register("{}" . format("proxyserver"), uri_proxy)
    print(uri_proxy)
    daemon.requestLoop()


if __name__ == '__main__':
    start_proxy('PYRONAME:transaction-manager@localhost:8888')
