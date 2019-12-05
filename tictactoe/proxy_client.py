import Pyro4


def connect(uri):
    proxy = Pyro4.Proxy(uri)

    print(proxy.get_list())


if __name__ == "__main__":
    connect("PYRO:obj_5b029e12616c44b1a9cd2ac09a57829b@localhost:63545")