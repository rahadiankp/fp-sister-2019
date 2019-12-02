import Pyro4

class RmConnector:
    
    host = None
    port = None
    uri = None
    
    instance = None

    def __init__(self):
        pass

    def set_connection(self, host, port):
        self.host = host
        self.port = port
        self.uri = "PYRONAME:replmanager@{}:{}" . format(self.host, str(self.port))
    
    def get_instance(self):
        if self.instance == None:
            self.setup()
        return self.instance
    
    def setup(self):
        self.instance = Pyro4.Proxy(self.uri)