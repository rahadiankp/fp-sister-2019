import Pyro4


if __name__ == "__main__":

    proxy = Pyro4.Proxy('PYRONAME:proxyserver-1@localhost:8888')
    
    while True:
        command = input()

        result = proxy.push_command(command)

        print(result)
