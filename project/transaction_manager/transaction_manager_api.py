
class TransactionManagerApi:

    data = []
    data_len = 0

    """
    :type data: dict @see util.CommandResolver
    """
    @staticmethod
    def push_command(command_data):
        TransactionManagerApi.data.append(command_data)
        TransactionManagerApi.data_len += 1
        print(TransactionManagerApi.data)

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
    def ping(self):
        return "PONG"
