from random import uniform
import pygame
from snake_obj import Snake
from food_obj import Food
from itertools import count

class Game:
    height = 600
    width = 800
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Steven\'s Snake... Hisss')

    clock = pygame.time.Clock()
    snake_block = 10
    snake_speed = 15

    #font_style = pygame.font.SysFont("bahnschrift", 25)
    #score_font = pygame.font.SysFont("comicsansms", 35)

    def __init__(self, learning=False):
        pygame.init()
        self.game_paused = False
        self.snake_x_change = 0
        self.snake_y_change = 0
        self.snake = Snake(self.height, self.width, 75)
        self.food = Food(self.height, self.width)
        self.learn() if learning else self.play()
        self.steps_taken = 0
        self.step_limit = 50

    '''def print_score(sel
        self.inputs = []

    def update(self, change_x, change_y):f, score):
        #value = self.score_font.render(str(score), True, self.yellow)
        #self.display.blit(value, [0, 0])
        #print(score)'''

    def draw_snake(self):
        for segment in self.snake.body:
            pygame.draw.rect(self.display, self.black,
                             [segment[0], segment[1],
                              self.snake_block, self.snake_block])

    def draw_food(self):
        pygame.draw.rect(self.display, self.red,
                         [self.food.pos_x, self.food.pos_y,
                          self.snake_block, self.snake_block])

    def snake_hit_food_check(self):
        if self.snake.pos_x == self.food.pos_x \
                and self.snake.pos_y == self.food.pos_y:
            self.food.new_position(self.height, self.width)
            self.snake.grow()

    def snake_hit_snake_check(self):
        for segment in self.snake.body[:-1]:
            if self.snake.head == segment:
                return True

    def snake_hit_wall_check(self):
        if self.snake.pos_x < 0 or self.snake.pos_x > self.width \
                or self.snake.pos_y < 0 or self.snake.pos_y > self.height:
            return True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                '''
                if self.game_paused:
                    self.game_paused = False
                '''
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_p:
                    self.snake_x_change = 0
                    self.snake_y_change = 0
                    self.game_paused = not self.game_paused
                    print("PAUSED")
                if event.key == pygame.K_a:
                    self.snake_x_change = -self.snake_block
                    self.snake_y_change = 0
                    self.snake.direction = 3
                elif event.key == pygame.K_d:
                    self.snake_x_change = self.snake_block
                    self.snake_y_change = 0
                    self.snake.direction = 1
                elif event.key == pygame.K_w:
                    self.snake_y_change = -self.snake_block
                    self.snake_x_change = 0
                    self.snake.direction = 0
                elif event.key == pygame.K_s:
                    self.snake_y_change = self.snake_block
                    self.snake_x_change = 0
                    self.snake.direction = 2
        return False

    def render(self):
        self.display.fill(self.white)
        self.draw_snake()
        self.draw_food()

    def collision(self):
        done = False
        if self.snake_hit_food_check():
            self.snake.reward = 100
        elif self.snake_hit_snake_check() or self.snake_hit_snake_check() or self.steps_taken > self.step_limit:
            self.snake.reward = -100
            done = True
        else:
            self.snake.reward = 1
        return self.snake.reward, done

    def step(self, action):
        if self.snake.direction == 0: # UP
            if action == 0: # left(left)
                self.snake_x_change = -self.snake_block
                self.snake_y_change = 0
                self.snake.direction = 3
            elif action == 1: # forward(up)
                self.snake_y_change = -self.snake_block
                self.snake_x_change = 0
                self.snake.direction = 0
            elif action == 2: # right(right)
                self.snake_x_change = self.snake_block
                self.snake_y_change = 0
                self.snake.direction = 1

        elif self.snake.direction == 1: # right
            if action == 0: # left(up)
                self.snake_y_change = -self.snake_block
                self.snake_x_change = 0
                self.snake.direction = 0
            elif action == 1: # forward(right)
                self.snake_x_change = self.snake_block
                self.snake_y_change = 0
                self.snake.direction = 1
            elif action == 2: # right(down)
                self.snake_y_change = self.snake_block
                self.snake_x_change = 0
                self.snake.direction = 2

        elif self.snake.direction == 2: # down
            if action == 0: # left(right)
                self.snake_x_change = self.snake_block
                self.snake_y_change = 0
                self.snake.direction = 1
            elif action == 1: # forward(down)
                self.snake_y_change = self.snake_block
                self.snake_x_change = 0
                self.snake.direction = 2
            elif action == 2: # right(left)
                self.snake_x_change = -self.snake_block
                self.snake_y_change = 0
                self.snake.direction = 3

        elif self.snake.direction == 3: # left
            if action == 0: # left(down)
                self.snake_y_change = self.snake_block
                self.snake_x_change = 0
                self.snake.direction = 2
            elif action == 1: # forward(left)
                self.snake_x_change = -self.snake_block
                self.snake_y_change = 0
                self.snake.direction = 3  
            elif action == 2: # right(up)
                self.snake_y_change = -self.snake_block
                self.snake_x_change = 0
                self.snake.direction = 0
        self.steps_taken += 1

        # return next_state, reward, done 
        return self.snake.look(self.food.pos_x, self.food.pos_y), self.collision()

    def learn(self, episodes=20):
        # reset the game
        self.__init__()
        state = None
        done = False
        self.render()
        for step in Count():
            # Decide on an action
            action = None
            if random.random() <= self.snake.brain.epsilon:
                action = random.randrange(self.snake.brain.num_actions)
            else:
                action = np.argmax(self.model.predict(state))
            # Make the action
            next_state, reward, done = self.step(action)

            self.snake.brain.replay
            

    def play(self):
        game_over = False

        while not game_over:
            self.display.fill(self.white)
            game_over = self.check_events()
            if not self.game_paused:
                self.snake.update(self.snake_x_change, self.snake_y_change)
            self.draw_snake()
            self.draw_food()
            self.snake_hit_food_check()
            if self.snake_hit_snake_check() or self.snake_hit_wall_check():
                game_over = True
                self.__init__()
            pygame.display.update()
            if not self.game_paused:
                self.snake.look(self.food.pos_x, self.food.pos_y)
            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()