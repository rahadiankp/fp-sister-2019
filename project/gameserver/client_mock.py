import Pyro4


def start_mock_client(uri_list: list):
    proxy_list = []

    for uri in uri_list:
        proxy_list.append(Pyro4.Proxy(uri))

    while True:
        pause = input()
        if pause != "reload":
            continue
        idx = 0
        for proxy in proxy_list:
            print("Server", idx)
            result: dict = proxy.verbose_server()
            bidx = 0
            for board in result:
                print("Board", bidx)
                print("  Player 1:", board['player_1'], "\n",
                      " Player 2:", board['player_2'], "\n",
                      " Board data:", board['board_data'])
                bidx += 1
            idx += 1


if __name__ == "__main__":
    proxy_list = ["PYRO:obj_9d12fa3510164767a770396957365ecb@localhost:64232"]
    start_mock_client(proxy_list)