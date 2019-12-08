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
            result = proxy.verbose_server()
            print(result['is_ready'])
            print(result['hash'])
            for i in range(2):
                print(result['player_list'][3*i], "||",
                      result['player_list'][3*i+1], "||",
                      result['player_list'][3*i+2])
            for row in result['board_state']:
                print(row)
            idx += 1


if __name__ == "__main__":
    proxy_list = [
        "PYRO:obj_b5cd856d04fe431cbc8670291ecd3ef3@localhost:60528",
        "PYRO:obj_4313aef4475948ce9bc33bf6364e63f4@localhost:60543",
        "PYRO:obj_05c7c5c039064e7aa756827ae7b13662@localhost:59510",
    ]
    start_mock_client(proxy_list)