# import pygame, sys, and Vector2 modules
import pygame
import sys
import random
from pygame.math import Vector2

# initialize pygame
pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

# colors in pygame are represented in tuples in rgb fashion
# initializes colors
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

# create grid
# stores size of each cell
cell_size = 20
# number of cells per row and grid
number_of_cells = 25

# Create a border around game window
# OFFSET determines width of the border
OFFSET = 75

# create food object
class Food:
    def __init__(self, snake_body):
        # set food position with Vector2 object (x,y)
        # Vector2 is a pygame method
        self.position = self.generate_random_pos(snake_body)

    # draw food on screen
    def draw(self):
        # define rect (x position, y position, width, height)
        # must multiply x and y positions by cell size since a grid is being used
        # draw method requires three arguments: surface, color, rect
        # the blit() method is used to draw the image on the screen
        # blit() requires 2 arguments: surface to draw, rect object that defines position and screen size
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y *
                                cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    # returns a random cell position
    # The randint() function returns a random number within a range
    # number_of_cells - 1 because one space is needed for the food object
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    # generate random position for food object
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

# Create a snake class


class Snake:
    def __init__(self):
        # how to represent the snake
        # body = [head cell, cell, cell]
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        # sets initial direction of the snake to the right
        self.direction = Vector2(1, 0)
        self.add_segment = False
        # self.eat_sound = pygame.mixer.Sound("FOLDER/filename.mp3")
        # self.wall_hit_sound = pygame.mixer.Sound("FOLDER/filename.mp3")

    # draw snake body
    def draw(self):
        # use for loop to draw all segments of snake body
        for segment in self.body:
            # fill a grid segment for each body segment
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            # draw rect on display surface, give DARK_GREEN color
            # 0 means the cell is filled completely and 7 is the border-radius of each cell
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    # update head cell position
    def update(self):
        # the insert method takes 2 arguments
        # 0 the index for the first element in the lst of body segments
        # moves head of snake in specified direction in direction attribute
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            # removes last segment of snake's body
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)

class Game:

    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self):
        self.snake.draw()
        self.food.draw()

    # update snake position, check for collisions
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    # make snake eat the food
    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            # self.snake.eat_sound.play()

    def check_collision_with_edges(self):
        # check if snake head reaches edge of screen
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()
            # self.snake.wall_hit_sound.play()

    def check_collision_with_tail(self):
        # creates new list containing only body segments minus the head
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()
            # self.snake.wall_hit_sound.play()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0

# creates display surface object named screen
# set_mode method takes a tuple as an argument, first value is width, second value is height
screen = pygame.display.set_mode((2*OFFSET + cell_size * number_of_cells, 2*OFFSET + cell_size * number_of_cells))

# give screen a title
pygame.display.set_caption("Retro Snake")

# create clock object
# controls frame rate of game
clock = pygame.time.Clock()

game = Game()

# The load image function takes filepath of image as function and
# returns a surface that is used to draw the image on the screen
# the r means 'raw' in other words, is a 'raw something, I cant remember. Look it up?'
food_surface = pygame.image.load(r"Graphics\food.png")

# USEREVENT is a pygame event type for creating custom events
# Event will be triggered when the snake's position needs updated
SNAKE_UPDATE = pygame.USEREVENT

# uses set_timer function from pygame
# creates a timer that triggers the SNAKE_UPDATE event every 200ms
# first arg: event that needs triggered, second arg is how often event is to be called
pygame.time.set_timer(SNAKE_UPDATE, 200)

# game loop
while True:
    # get all events pygame recognizes
    for event in pygame.event.get():

        # check for any events that happened since last time loop was executed
        # this ensures the snake only moves when SNAKE_UPDATE is called
        # to avoid the event from being called at 60 fps
        if event.type == SNAKE_UPDATE:
            game.update()

        # defines a way to break out of while loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # add pygame keydown event listener to control snake
        # determine which key is pressed using the event.key attribute
        # using the and operator ensures the snake cannot change direction into itself
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # screen.fill fills the canvas with a defined color as an argument
    screen.fill(GREEN)
    # pygame.draw.rect requires 4 arguments (surface, color, rect, border_size)
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cell_size*number_of_cells+10,
                                          cell_size*number_of_cells+10), 5)
    # draw the game
    game.draw()
    title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET-5, 20))
    screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size*number_of_cells + 10))

    # update the system outside the for loop
    pygame.display.update()

    # the tick method takes an integer as an argument and the integer is the fps we want
    # this means the while loop runs 60x per second
    # setting the frame rate ensures consistency
    clock.tick(60)
