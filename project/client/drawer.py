import pygame
import sys
import pprint
import time
import threading


class Drawer:

    GUIBOARD_LEFT = 40  # in px
    GUIBOARD_UP = 40    # in px

    GUIBOARD_RECTSIZE = 80  # in px
    GUIBOARD_OFFSET = 0     # in px

    board = None
    is_turn = False
    game_status_text = ''

    # pygame
    # pygame config, used for game setting
    RESOLUTION = (800, 560)
    # end of game setting
    # pygame variable
    screen = None
    resource = None
    my_piece = None
    drawn = None
    status_surface = None
    # end of pygame variable

    def __init__(self, board, username: str, board_id: str, player_id: int, proxy):
        self.board = board
        self.username = username
        self.board_id = board_id
        self.player_id = player_id
        self.proxy = proxy
        self.game_status_text = "Welcome to Dic-Dac-Doe!"

        player_num = "1st Player" if self.player_id == 0 else "2nd Player"
        self.title = "TicTacToe - " + username + " - Board " + board_id + " - " + player_num

        # need self.drawn initialization here
        # pprint.pprint(board)
        self.drawn = self.board.board_data.copy()
        self.load_resource()
        self.init_drawn()
        self.init_pygame()

        self.update_running = True
        self.update_thread = threading.Thread(target=self.update_board_threaded)
        self.update_thread.start()

        self.check_running = True
        self.check_thread = threading.Thread(target=self.check_board_thread)
        self.check_thread.start()

    def update_screen(self):
        running = True
        mousepx = None
        try:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # event unregister
                        unregister_response = self.proxy.push_command(
                            "UNREGISTER " + self.username + " " + self.board_id)
                        self.update_running = False
                        self.update_thread.join()
                        self.check_running = False
                        # self.check_thread.join()
                        running = False
                        break
                    
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousepx = pygame.mouse.get_pos()
                        self.place_piece(mousepx)

                    self.draw()
                    pygame.display.update()
        except KeyboardInterrupt:
            sys.exit()

    def load_resource(self):
        self.resource = {}
        
        # load all resource here
        self.resource.update({'board': pygame.image.load('assets/board.png')})
        self.resource.update({'O': pygame.image.load('assets/red_o.png')})
        self.resource.update({'X': pygame.image.load('assets/blue_x.png')})
        for i in range(0,6):
            asset_name = 'assets/play' + str(i) + '.png'
            self.resource.update({'board_dim_'+str(i) : pygame.image.load(asset_name)})

    def draw(self): # will be threaded
        self.draw_board()
        self.draw_piece()
        # create function for every feature to be drawn
        self.draw_game_status()
        self.draw_dim()

    def draw_board(self): # draw visualization of board without piece
        self.screen.blit(self.resource['board'], (0, 0))

    def draw_dim(self):
        dim_str = 'board_dim_' + str(self.board_id)
        self.screen.blit(self.resource[dim_str], (0, 0))

    def draw_piece(self): # draw board's piece
        for row in self.drawn:
            for data in row:
                if data[0] == '-' or data[1] == None:
                    continue
                self.screen.blit(data[0], data[1])

    def draw_game_status(self):
        self.status_surface = self.font.render(self.game_status_text, False, (0,0,0))
        self.screen.blit(self.status_surface, (100, 5))

    def get_pivot_pixel(self, pixel): # get pivot pixel (upper left) of board's rectangle
        x = ( (pixel[0] - self.GUIBOARD_LEFT) // self.GUIBOARD_RECTSIZE ) * self.GUIBOARD_RECTSIZE
        y = ( (pixel[1] - self.GUIBOARD_UP) // self.GUIBOARD_RECTSIZE ) * self.GUIBOARD_RECTSIZE

        return [x, y]

    # transpose position according to ID
    def transpose_coordinate_by_id(self, coordinate, server_id):
        id = server_id
        col, row = 0, 0
        if id == 0:
            col -= 0
            row -= 0
        elif id == 1:
            col -= 3
            row -= 0
        elif id == 2:
            col -= 6
            row -= 0
        elif id == 3:
            col -= 0
            row -= 3
        elif id == 4:
            col -= 3
            row -= 3
        elif id == 5:
            col -= 6
            row -= 3

        return [coordinate[0] + col, coordinate[1] + row]

    def get_board_id_by_coordinate(self, coordinate):
        if coordinate[0] >= 1 and coordinate[0] <= 3:
            if coordinate[1] >= 1 and coordinate[1] <= 3:
                return 0
            if coordinate[1] >= 4 and coordinate[1] <= 6:
                return 3
        if coordinate[0] >=4 and coordinate[0] <= 6:
            if coordinate[1] >= 1 and coordinate[1] <= 3:
                return 1
            if coordinate[1] >= 4 and coordinate[1] <= 6:
                return 4
        if coordinate[0] >=6 and coordinate[0] <= 9:
            if coordinate[1] >= 1 and coordinate[1] <= 3:
                return 2
            if coordinate[1] >= 4 and coordinate[1] <= 6:
                return 5

    def update_board_threaded(self):
        while self.update_running:
            time.sleep(0.5)
            try:
                self.drawn = self.proxy.push_command("UPDATE")['data']
                self.init_drawn()
            except:
                pass

    def check_board_thread(self):
        stop_response = ["DRAW", "WIN"]
        while self.check_running:
            time.sleep(2)
            try:
                check_response: dict = self.proxy.push_command("CHECK " + self.username + " " + self.board_id)
                prefix_title = check_response['message']
            except:
                continue
            # text for status
            self.game_status_text = self.get_status_message(check_response['message'])
            if prefix_title.split()[0] in stop_response:
                self.proxy.push_command("RPOL " + self.username + " " + self.board_id)
                time.sleep(1)
                pygame.event.post(pygame.event.Event(pygame.QUIT, {}))
                break

    def get_status_message(self, message):
        command = message.split()[0]
        if command == "NTRN":
            return "Wait for turn..."
        elif command == "TURN":
            return "Place your piece..."
        elif command == "NPLYR":
            return "Not part of the board, can not make a move..."
        elif command == "NST":
            return "Game not started yet, please wait for opponent..."
        elif command == "DRAW":
            return "DRAW! Exiting Game..."
        elif command == "BAD":
            return "Place somewhere else!"
        elif command == "WIN":
            player_id = message.split()[2]
            if int(player_id) == self.player_id:
                return "YOU WIN! Exiting Game..."
            return "YOU LOSE! Exiting Game..."
        elif command == "NSRV":
            return "Connection to server lost..."
        else:
            return "WEIRD MESSAGE"

    def position_to_pixel(self, coordinate):
        col = coordinate[0] - 1
        row = coordinate[1] - 1
        x = self.GUIBOARD_LEFT + self.GUIBOARD_RECTSIZE * col + self.GUIBOARD_OFFSET
        y = self.GUIBOARD_UP + self.GUIBOARD_RECTSIZE * row + self.GUIBOARD_OFFSET - 5

        return [x, y]

    def position_to_coordinate(self, pixel):
        x = pixel[0] - self.GUIBOARD_LEFT
        y = pixel[1] - self.GUIBOARD_UP
        col = x // self.GUIBOARD_RECTSIZE + 1
        row = y // self.GUIBOARD_RECTSIZE + 1

        return [col, row]
    
    def place_piece(self, pixel):
        coordinate = self.position_to_coordinate(pixel)

        # out of board mouse click
        if coordinate[0] < 1 or coordinate[0] > 9 or coordinate[1] < 1 or coordinate[1] > 6:
            return

        # generate command string here (to be saved to TM)
        server_id = self.get_board_id_by_coordinate(coordinate)
        server_coordinate = self.transpose_coordinate_by_id(coordinate, server_id)
        cmd = 'PUT {} {} {},{}'.format(self.username,
                                       server_id,
                                       str(server_coordinate[0]-1), str(server_coordinate[1]-1))
        put_response = self.proxy.push_command(cmd)
        if put_response['status'] != "OK":
            print(put_response['message'])
            self.game_status_text = self.get_status_message(put_response['message'])
            return
        piece = put_response['message'].split()[1]
        self.board.board_data[coordinate[1]-1][coordinate[0]-1] = piece
        self.update_drawn(self.position_to_pixel(coordinate), coordinate, piece)

    # set pygame config
    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.status_surface = self.font.render(self.game_status_text, False, (0,0,0))
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode(self.RESOLUTION)
                
    def init_drawn(self):
        for row in range(0, 6):
            for column in range(0, 9):
                pix = self.position_to_pixel([column+1, row+1])
                if self.drawn[row][column] == '-':
                    self.drawn[row][column] = ['-', None]
                elif self.drawn[row][column] == 'X':
                    self.drawn[row][column] = [self.resource['X'].copy(), pix]
                elif self.drawn[row][column] == 'O':
                    self.drawn[row][column] = [self.resource['O'].copy(), pix]

    def update_drawn(self, pixel, coordinate, piece):
        self.drawn[coordinate[1]-1][coordinate[0]-1] = [self.resource[piece].copy(), pixel]