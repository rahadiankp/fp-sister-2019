import Pyro4

from project.transaction_manager.transaction_manager_api import TransactionManagerApi
from project.util.command_resolver import CommandResolver


@Pyro4.behavior(instance_mode="single")
class ProxyServerApi:

    non_transaction_command = ['START', 'CHECK', 'UPDATE']
    tm_uri = 'PYRONAME:transaction-manager@localhost:8888'
    tm: TransactionManagerApi = Pyro4.Proxy(tm_uri)

    server_api_list = []
    last_index_call = 0

    fail_response = {'status': 'FAILED'}

    @staticmethod
    def push_command(command: str):
        command_data = CommandResolver.resolve_command(command)
        last_index_call = ProxyServerApi.last_index_call
        ProxyServerApi.last_index_call += 1

        if len(ProxyServerApi.server_api_list):
            return ProxyServerApi.fail_response

        try:
            server_response = ProxyServerApi.server_api_list[last_index_call].push_command(command_data)
            if server_response['status'] == 'OK':
                ProxyServerApi.tm.push_command(command_data)
                for i, server in enumerate(ProxyServerApi.server_api_list):
                    if i == last_index_call:
                        continue
                    server.push_command(command_data)

            else:
                return ProxyServerApi.fail_response

            if command_data['action'] not in ProxyServerApi.non_transaction_command:
                ProxyServerApi.tm.push_command(command_data)

        except():
            return ProxyServerApi.fail_response

    @staticmethod
    def register_server(server_uri):
        ProxyServerApi.server_api_list.append(
            Pyro4.Proxy(server_uri)
        )

