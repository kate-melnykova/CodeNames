import os
import glob
from random import randint
from uuid import uuid4

from config import images_loc

#filenames = list(glob.glob(os.path.join(images_loc,'*.*')))
filenames = list(range(100))


class Board:
    n_rows = 5
    n_cols = 5
    n_entries = 25
    n_red = 8
    n_blue = 8

    def __init__(self):
        # get 25 non-repetitive entries from 0 to 99
        selected = 0
        board_images = list()
        len_files = len(filenames)
        while selected < self.n_entries:
            i = randint(0, len_files - 1)
            if i not in board_images:
                board_images.append(i)
                selected += 1
        board_images = [filenames[idx] for idx in board_images]

        # assign the color of keycard
        turn = randint(0, 1)
        if turn:
            self.n_red += 1
            self.turn = 'r'
        else:
            self.n_blue += 1
            self.turn = 'b'

        # assign random colors
        board_colors = ['w'] * self.n_entries
        board_colors[randint(0, self.n_entries - 1)] = 'k'  # black
        red_cards = 0
        while red_cards < self.n_red:
            i = randint(0, self.n_entries - 1)
            if board_colors[i] == 'w':
                board_colors[i] = 'r'
                red_cards += 1
        blue_cards = 0
        while blue_cards < self.n_blue:
            i = randint(0, self.n_entries - 1)
            if board_colors[i] == 'w':
                board_colors[i] = 'b'
                blue_cards += 1

        # merge data and store it as n_rows - by - n_cols board
        board = list(zip(board_images, board_colors, [0]*self.n_entries))
        self.board = []
        idx = 0
        for i in range(self.n_rows):
            self.board.append(board[idx:idx + self.n_rows])
            idx += self.n_rows

    def reveal(self, i: int, j: int) -> str:
        im, col, hidden = self.board[i][j]
        self.board[i][j] = [im, col, 1]
        return col


class Game:
    def __init__(self):
        self.id = str(uuid4())[:4]
        self.board = Board()
        self.all_users = []
        self.potential_codemasters = []
        self.red_team = []
        self.blue_team = []
        self.codemaster_red = None
        self.codemaster_blue = None
        self.turn = self.board.turn
        self.status = 0 # 0 for waiting for players, 1 for playing, 2 for completed

    def add_player(self, name: str, wants_codemaster: bool):
        self.all_users.append(name)
        if wants_codemaster:
            self.potential_codemasters.append(name)

    def start(self):
        assert self.all_users > 3
        self.status = 1
        if not self.potential_codemasters:
            i = randint(0, len(self.all_users) - 1)
            self.codemaster_red = self.all_users.pop(i)
            i = randint(0, len(self.all_users) - 1)
            self.codemaster_blue = self.all_users.pop(i)
        elif len(self.potential_codemasters) == 1:
            i = randint(0, len(self.potential_codemasters) - 1)
            self.codemaster_red = self.potential_codemasters.pop(i)
            self.all_users.remove(self.codemaster_red)
            i = randint(0, len(self.all_users) - 1)
            self.codemaster_blue = self.all_users.pop(i)
        else:
            i = randint(0, len(self.potential_codemasters) - 1)
            self.codemaster_red = self.potential_codemasters.pop(i)
            self.all_users.remove(self.codemaster_red)
            i = randint(0, len(self.potential_codemasters) - 1)
            self.codemaster_blue = self.potential_codemasters.pop(i)
            self.all_users.remove(self.codemaster_blue)

        for _ in range(len(self.all_users) // 2):
            i = randint(self.all_users)
            self.red_team.append(self.all_users.pop(i))
        self.blue_team = list(self.all_users)





