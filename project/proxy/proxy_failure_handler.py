import os
import signal
import threading
import time
import Pyro4
import atexit
import psutil

from project.proxy.proxy_server import start_proxy
from project.proxy.proxy_server_api import ProxyServerApi


# pyro4-ns -n localhost -p 8888

class HeartBeatChecker(threading.Thread):

    def __init__(self, proxy_uri, tm_uri):
        threading.Thread.__init__(self)
        self.proxy_uri = proxy_uri
        proxy_server: ProxyServerApi = Pyro4.Proxy(proxy_uri)
        self.proxy = proxy_server
        self.tm_uri = tm_uri
        self.is_on_start = False

    def turn_on_proxy(self):

        if self.is_on_start:
            self.proxy = Pyro4.Proxy(self.proxy_uri)
            self.is_on_start = False
            print('connected')

        else:
            self.is_on_start = True
            n = os.fork()
            if n == 0:
                start_proxy(self.tm_uri)

    def run(self):
        while True:
            time.sleep(2)
            if self.is_on_start:
                print('continue')
                self.turn_on_proxy()
                continue
            try:
                print('try ping')
                self.proxy.ping()
                print('success ping')
            except:
                print('failed ping')
                self.turn_on_proxy()


def on_exit():
    parent = psutil.Process(os.getpid())
    children = parent.children(recursive=True)
    for process in children:
        process.send_signal(signal.SIGTERM)


if __name__ == '__main__':
    HeartBeatChecker('PYRONAME:proxyserver@localhost:8888', 'PYRONAME:transaction-manager@localhost:8888').start()
    atexit.register(on_exit)
