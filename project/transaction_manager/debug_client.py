import Pyro4


def start_mock_client(uri_list: list):
    tm_proxy_list = []

    for uri in uri_list:
        tm_proxy_list.append(Pyro4.Proxy(uri))

    while True:
        pause = input()
        if pause != "reload":
            continue
        idx = 0
        for proxy in tm_proxy_list:
            print("TM", idx)
            result = proxy.verbose_server()
            print(result)
            idx += 1


if __name__ == "__main__":
    tm_list = [
        "PYRONAME:tm-1@localhost:8888",
        "PYRONAME:tm-2@localhost:8888",
        "PYRONAME:tm-3@localhost:8888",
    ]
    start_mock_client(tm_list)
