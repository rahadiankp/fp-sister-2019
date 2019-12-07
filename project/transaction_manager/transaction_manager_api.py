import Pyro4
import hashlib


class TransactionManagerApi:

    data = []
    data_len = 0

    """
    :type data: dict @see util.CommandResolver
    """
    @staticmethod
    @Pyro4.oneway
    def push_command(command_data):
        TransactionManagerApi.data.append(command_data)
        TransactionManagerApi.data_len += 1
        # print(TransactionManagerApi.data)

    @staticmethod
    def get_all_data():
        return TransactionManagerApi.data

    @staticmethod
    def get_data_length():
        return TransactionManagerApi.data_len

    @staticmethod
    def get_data_to_last_from(index):
        return TransactionManagerApi.data[index:]

    @staticmethod
    def ping():
        return "PONG"

    """Debug methods

    """

    @staticmethod
    def verbose_server():
        length = TransactionManagerApi.data_len
        length_data = len(TransactionManagerApi.data)
        hash_value = hashlib.md5("EMPTY TRANSACTION".encode())
        for data in TransactionManagerApi.data:
            print(data)
            hash_value = hashlib.md5((hash_value.hexdigest() + str(data)).encode())

        return {
            'len': length,
            'len_data': length_data,
            'hash': hash_value.hexdigest(),
        }

