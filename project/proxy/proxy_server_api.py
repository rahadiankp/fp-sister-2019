# from project.util.command_resolver import CommandResolver
import threading
import time
import Pyro4
import Pyro4.errors
import command_resolver


@Pyro4.behavior(instance_mode="session")
class ProxyServerApi:

    def __init__(self):
        self.non_transaction_command = ['CHECK', 'UPDATE']

        self.tm_list = []
        # self.tm_list = [Pyro4.Proxy(uri) for uri in tm_uri_list]
        # self.tm: TransactionManagerApi = Pyro4.Proxy(tm_uri_list)

        self.tm_uri_list = []
        self.server_api_list = []
        self.last_index_call = 0

        self.game_server_failure_detection_thread = {}
        self.tm_failure_detection_thread = {}

        self.fail_response_no_server = {'status': 'FAILED', 'message': 'NSRV No servers available'}

    def _push_to_tm(self, command):
        for uri in self.tm_uri_list:
            try:
                proxy = Pyro4.Proxy(uri)
                if proxy.is_ready():
                    proxy.push_command(command)
            except:
                pass

    @Pyro4.expose
    def get_transaction_manager_uri(self):
        for uri in self.tm_uri_list:
            try:
                proxy = Pyro4.Proxy(uri)
                proxy.ping()
                if proxy.is_ready():
                    return uri
            except Exception as e:
                print(e)
                pass

    @Pyro4.expose
    def push_command(self, command: str):
        # print('before')
        command_data = command_resolver.CommandResolver.resolve_command(command)
        last_index_call = self.last_index_call
        self.last_index_call += 1
        if command_data['action'] not in self.non_transaction_command:
            print("Recvd command:", command_data)
        if self.last_index_call >= len(self.server_api_list):
            self.last_index_call = 0

        # print(last_index_call)
        # print(len(self.server_api_list))

        if len(self.server_api_list) == 0:
            return self.fail_response_no_server

        try:
            server_proxy_last = Pyro4.Proxy(self.server_api_list[last_index_call])
            server_response = server_proxy_last.push_command(command_data)
            if server_response['status'] == 'OK':
                for i, server_uri in enumerate(self.server_api_list):
                    server_proxy = Pyro4.Proxy(server_uri)
                    if i == last_index_call:
                        continue
                    server_proxy.push_command(command_data)

                if command_data['action'] not in self.non_transaction_command:
                    self._push_to_tm(command_data)

                return server_response
            else:
                return server_response

        except Exception as e:
            print(e)
            print('ada error')
            self.server_api_list.pop(last_index_call)
            self.last_index_call = 0
            return self.push_command(command)

    @Pyro4.expose
    def ping(self):
        return "PONG"

    @Pyro4.oneway
    @Pyro4.expose
    def register_server(self, server_uri):
        self.server_api_list.append(
            server_uri
        )

        print('[GS]Registered -', server_uri)

        # start ping failure detection thread
        pfd = threading.Thread(target=self.ping_game_server, args=(server_uri,))
        self.game_server_failure_detection_thread[server_uri] = pfd
        pfd.start()

    def remove_server(self, server_uri):
        print("[GS] Failure Detector has detected", server_uri, "is down")

        # self.game_server_failure_detection_thread.pop(server_uri)

        self.last_index_call = 0
        self.server_api_list.remove(server_uri)
        print("[GS] Unregistered -", server_uri)

    def ping_game_server(self, game_server_uri: str):
        print("[GS] Monitoring -", game_server_uri)
        while True:
            time.sleep(2)
            try:
                proxy = Pyro4.Proxy(game_server_uri)
                proxy.ping()
            except Pyro4.errors.CommunicationError as e:
                # print(e)
                break
        self.remove_server(game_server_uri)

    @Pyro4.oneway
    @Pyro4.expose
    def register_tm(self, tm_uri):
        self.tm_uri_list.append(tm_uri)

        print('[TM] Registered -', tm_uri)

        # start ping failure detection thread
        pfd = threading.Thread(target=self.ping_tm, args=(tm_uri,))
        self.tm_failure_detection_thread[tm_uri] = pfd
        pfd.start()

    def remove_tm(self, tm_uri):
        print("[TM] Failure Detector has detected", tm_uri, "is down")

        # self.tm_failure_detection_thread.pop(tm_uri)

        self.last_index_call = 0
        self.tm_uri_list.remove(tm_uri)
        print("[TM] Unregistered -", tm_uri)

    def ping_tm(self, tm_uri: str):
        print("[TM] Monitoring -", tm_uri)
        while True:
            time.sleep(2)
            try:
                proxy = Pyro4.Proxy(tm_uri)
                proxy.ping()
            except Pyro4.errors.CommunicationError as e:
                # print(e)
                break
        self.remove_tm(tm_uri)
