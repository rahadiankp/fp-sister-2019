import sys
import board
import drawer
import rmconnector
import threading

class Client:
    
    board = None
    drawer = None

    def __init__(self):
        self.board = board.Board()
        # ==== need to fetch board data from game server

        # ====
        self.drawer = drawer.Drawer()

    @staticmethod
    def start():
        pass

if __name__ == "__main__":
    Client.start()