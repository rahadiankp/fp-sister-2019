import threading
import time

import Pyro4
import Pyro4.errors

from project.util.command_resolver import CommandResolver


@Pyro4.behavior(instance_mode="single")
class ProxyServerApi:

    def __init__(self, tm_uri_list):
        self.non_transaction_command = ['CHECK', 'UPDATE']

        self.tm_uri = tm_uri_list
        self.tm_list = [Pyro4.Proxy(uri) for uri in tm_uri_list]
        # self.tm: TransactionManagerApi = Pyro4.Proxy(tm_uri_list)

        self.server_api_list = []
        self.last_index_call = 0

        self.game_server_failure_detection_thread = {}

        self.fail_response_no_server = {'status': 'FAILED', 'message': 'No servers available'}

    def _push_to_tm(self, command):
        tm_count = len(self.tm_list)

        for i in range(tm_count):
            self.tm_list[i].push_command(command)

    @Pyro4.expose
    def get_transaction_manager_uri(self):
        for tm in self.tm_list:
            try:
                tm.ping()
                return tm
            except:
                pass

    @Pyro4.expose
    def push_command(self, command: str):
        # print('before')
        command_data = CommandResolver.resolve_command(command)
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
                    #self.tm.push_command(command_data)
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

    @Pyro4.expose
    def register_server(self, server_uri):
        self.server_api_list.append(
            server_uri
        )

        # start ping failure detection thread
        pfd = threading.Thread(target=self.ping_game_server, args=(server_uri,))
        self.game_server_failure_detection_thread[server_uri] = pfd
        pfd.start()

        print('Registered -', server_uri)

    def remove_server(self, server_uri):
        print("Failure Detector has detected", server_uri, "is down")

        # join pfd thread to main thread
        # pfd_t = self.game_server_failure_detection_thread[server_uri]
        # pfd_t.join()

        self.last_index_call = 0
        self.server_api_list.remove(server_uri)
        print("Unregistered -", server_uri)

    def ping_game_server(self, game_server_uri: str):
        print("Monitoring -", game_server_uri)
        while True:
            time.sleep(2)
            try:
                proxy = Pyro4.Proxy(game_server_uri)
                ping_response = proxy.ping()
            except Pyro4.errors.CommunicationError as e:
                print(e)
                break
        self.remove_server(game_server_uri)

