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
    proxy_list = ["PYRO:obj_d30d379a5a0b41ff99dc6acb22192eb3@localhost:63617",
                  "PYRO:obj_890ed6f50a5044a8b87e3c3b6ca4a83a@localhost:63626",
                  "PYRO:obj_26a96cf8e35a47c2849ddc116e37b5c1@localhost:63635"]
    start_mock_client(proxy_list)