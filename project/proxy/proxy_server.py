from project.proxy.proxy_server_api import ProxyServerApi
import getopt
import Pyro4
import sys

# pyro4-ns -n localhost -p 8888


def start_proxy(tm_uri, name, host, port):
    daemon = Pyro4.Daemon(host=host)
    ns = Pyro4.locateNS(host,port)
    proxy_server_api = ProxyServerApi(tm_uri)
    uri_proxy = daemon.register(proxy_server_api)
    ns.register("{}" . format(name), uri_proxy)
    print(uri_proxy)
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
    print(NAME, HOST, PORT)
    start_proxy('PYRONAME:transaction-manager@localhost:8888',
                NAME,
                HOST,
                PORT)
