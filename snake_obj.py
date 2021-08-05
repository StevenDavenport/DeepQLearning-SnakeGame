import math
from brain_obj import Brain

class Snake:
    def __init__(self, game_height, game_width, length):
        self.direction = 0
        self.head = []
        self.body = []
        self.game_height = game_height
        self.game_width = game_width
        self.pos_x = self.game_width / 2
        self.pos_y = self.game_height / 2
        self.length = length
        self.inputs = []
        self.brain = Brain()

    def update(self, change_x, change_y):
        self.head = []
        self.pos_x += change_x
        self.pos_y += change_y
        self.head.append(self.pos_x)
        self.head.append(self.pos_y)
        self.body.append(self.head)
        if len(self.body) > self.length:
            del self.body[0]

    def look_left(self):
        distance_from_collision = abs(0 - self.pos_x)
        for segment in self.body[:-1]:
            if self.pos_y == segment[1]:
                if segment[0] < self.pos_x:
                    if abs(segment[0] - self.pos_x) < distance_from_collision:
                        distance_from_collision = abs(segment[0] - self.pos_x)
        print(" Left: ", distance_from_collision)
        return distance_from_collision

    def look_right(self):
        distance_from_collision = abs(self.game_width - self.pos_x)
        for segment in self.body[:-1]:
            if self.pos_y == segment[1]:
                if segment[0] > self.pos_x:
                    if abs(segment[0] - self.pos_x) < distance_from_collision:
                        distance_from_collision = abs(segment[0] - self.pos_x)
        print(" Right: ", distance_from_collision)
        return distance_from_collision
        
    def look_up(self):
        distance_from_collision = abs(0 - self.pos_y)
        for segment in self.body[:-1]:
            if self.pos_x == segment[0]:
                if segment[1] < self.pos_y:
                    if abs(segment[1] - self.pos_y) < distance_from_collision:
                        distance_from_collision = abs(segment[1] - self.pos_y)
        print(" Up: ", distance_from_collision)
        return distance_from_collision

    def look_down(self):
        distance_from_collision = abs(self.game_height - self.pos_y)
        for segment in self.body[:-1]:
            if self.pos_x == segment[0]:
                if segment[1] > self.pos_y:
                    if abs(segment[1] - self.pos_y) < distance_from_collision:
                        distance_from_collision = abs(segment[1] - self.pos_y)
        print(" Down: ", distance_from_collision)
        return distance_from_collision

    def look_food(self, x, y):
        distance_from_food_x = x - self.pos_x
        distance_from_food_y = y - self.pos_y
        distance_from_food = math.sqrt((distance_from_food_x ** 2) + (distance_from_food_y ** 2))
        print(" Food: ", distance_from_food)

    def look(self, x, y):
        if self.direction == 0:
            self.look_left()
            self.look_up()
            self.look_right()
        if self.direction == 1:
            self.look_up()
            self.look_right()
            self.look_down()
        if self.direction == 2:
            self.look_right()
            self.look_down()
            self.look_left()
        if self.direction == 3:
            self.look_down()
            self.look_left()
            self.look_up()
        self.look_food(x, y)

    def grow(self):
        self.length += 1

