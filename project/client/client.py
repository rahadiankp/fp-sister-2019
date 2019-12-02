import sys
import board
import drawer
import rmconnector
import threading

import pprint

class Client:
    
    board = None
    drawer = None

    def __init__(self):
        # ==== need to fetch board data from game server
        fetch = [
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
                    ['-', '-', '-', '-', '-', '-', '-', '-', '-']
        ]
        # ====
        # this client's player piece ('o' or 'x') used as parameter below
        self.board = board.Board(fetch)
        temp = 'x'
        self.drawer = drawer.Drawer(self.board, temp)

    def start(self):
        self.drawer.update_screen()

if __name__ == "__main__":
    client = Client()
    client.start()