import Pyro4
import hashlib


@Pyro4.behavior(instance_mode="session")
class TransactionManagerApi:

    def __init__(self, own_uri, proxy_uri_list, is_bootstrap):
        self.own_uri = own_uri
        self.proxy_uri_list = proxy_uri_list
        self.data = []
        self.data_len = 0

        self.is_bootstrap = is_bootstrap
        self.ready = False

        self.register_to_proxy()

    def register_to_proxy(self):
        for uri in self.proxy_uri_list:
            try:
                proxy = Pyro4.Proxy(uri)
                proxy.register_tm(self.own_uri)
            except:
                pass

        if self.is_bootstrap:
            self.ready = True
            return

        tm_uri_peer = None
        for uri in self.proxy_uri_list:
            try:
                proxy = Pyro4.Proxy(uri)
                tm_uri_peer = proxy.get_transaction_manager_uri()
                break
            except:
                pass

        up_to_date = False
        from_index = 0
        tm_peer_proxy = Pyro4.Proxy(tm_uri_peer)
        commands = tm_peer_proxy.get_data_to_last_from(from_index)
        latest_len = len(commands)

        while not up_to_date:
            for command in commands:
                self.push_command(command)

            new_latest_len = tm_peer_proxy.get_data_length()
            up_to_date = new_latest_len == latest_len
            from_index = latest_len - 1
            latest_len = new_latest_len
            if not up_to_date:
                commands = tm_peer_proxy.get_data_to_last_from(from_index)

        self.ready = True

    @Pyro4.expose
    def is_ready(self):
        return self.ready

    @Pyro4.oneway
    @Pyro4.expose
    def push_command(self, command_data):
        self.data.append(command_data)
        self.data_len += 1

    @Pyro4.expose
    def get_all_data(self):
        return self.data

    @Pyro4.expose
    def get_data_length(self):
        return self.data_len

    @Pyro4.expose
    def get_data_to_last_from(self, index):
        return self.data[index:]

    @Pyro4.expose
    def ping(self):
        return "PONG"

    """Debug methods

    """

    @Pyro4.expose
    def verbose_server(self):
        length = self.data_len
        length_data = len(self.data)
        is_bootstrap = self.is_bootstrap
        ready = self.ready
        hash_value = hashlib.md5("EMPTY TRANSACTION".encode())
        for data in self.data:
            print(data)
            hash_value = hashlib.md5((hash_value.hexdigest() + str(data)).encode())

        return {
            'len': length,
            'len_data': length_data,
            'hash': hash_value.hexdigest(),
            'ready': ready,
            'is_bootstrap': is_bootstrap,
        }

