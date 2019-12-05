import Pyro4
from project.proxy.proxy_server_api import ProxyServerApi

if __name__ == "__main__":

    proxy: ProxyServerApi = Pyro4.Proxy('PYRONAME:proxyserver@localhost:8888')
    
    while True:
        command = input()

        result = proxy.push_command(command)

        print(result)
