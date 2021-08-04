import pygame
from snake_obj import Snake
from food_obj import Food


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

    def __init__(self):
        pygame.init()
        self.game_paused = False
        self.snake_x_change = 0
        self.snake_y_change = 0
        self.snake = Snake(self.height, self.width, 75)
        self.food = Food(self.height, self.width)
        self.play()

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
                if self.game_paused:
                    self.game_paused = False
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