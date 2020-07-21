import random


class Food:
    def __init__(self, height_of_board, width_of_board):
        self.pos_x = 0
        self.pos_y = 0
        self.new_position(height_of_board, width_of_board)

    def new_position(self, height_of_board, width_of_board):
        self.pos_x = round(random.randrange(0, width_of_board - 10) / 10.0) * 10.0
        self.pos_y = round(random.randrange(0, height_of_board - 10) / 10.0) * 10.0
