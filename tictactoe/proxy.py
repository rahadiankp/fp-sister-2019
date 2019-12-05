import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Proxy(object):

    def __init__(self):
        self.connected_game_servers = []
        self.connected_clients = []

    def announce_server(self, server_uri: str):
        self.list_msg.append(msg)

    def get_list(self):
        return self.list_msg
