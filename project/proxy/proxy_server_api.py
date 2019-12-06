import Pyro4

from project.transaction_manager.transaction_manager_api import TransactionManagerApi
from project.util.command_resolver import CommandResolver


@Pyro4.behavior(instance_mode="single")
class ProxyServerApi:

    def __init__(self, tm_uri):
        self.non_transaction_command = ['CHECK', 'UPDATE']

        self.tm_uri = tm_uri
        self.tm: TransactionManagerApi = Pyro4.Proxy(tm_uri)

        self.server_api_list = []
        self.last_index_call = 0

        self.fail_response = {'status': 'FAILED'}

    @Pyro4.expose
    def get_transaction_manager_uri(self):
        return self.tm_uri

    @Pyro4.expose
    def push_command(self, command: str):
        print('before')
        command_data = CommandResolver.resolve_command(command)
        last_index_call = self.last_index_call
        self.last_index_call += 1
        print(command_data)
        if self.last_index_call >= len(self.server_api_list):
            self.last_index_call = 0

        print(last_index_call)
        print(len(self.server_api_list))

        if len(self.server_api_list) == 0:
            return self.fail_response

        try:
            server_response = self.server_api_list[last_index_call].push_command(command_data)
            if server_response['status'] == 'OK':
                for i, server in enumerate(self.server_api_list):
                    if i == last_index_call:
                        continue
                    server.push_command(command_data)

                if command_data['action'] not in self.non_transaction_command:
                    self.tm.push_command(command_data)

                return server_response
            else:
                return self.fail_response

        except:
            print('ada error')
            self.server_api_list.pop(last_index_call)
            self.last_index_call = 0
            return self.push_command(command)

    @Pyro4.expose
    def register_server(self, server_uri):
        self.server_api_list.append(
            Pyro4.Proxy(server_uri)
        )
        print('registered')
