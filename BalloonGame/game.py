import pygame
import random
import time

""""
Pygame is the game module being used for displaying the screen containing the balloons, score, and time.
Random is the random number generation module being used for the purpose of randomizing certain variables.
Time is the standard in-built python library used for time functions. 
"""

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:

    #  Game screen variables.
    disp_width = 1900
    disp_height = 1000
    left_boundary = 250
    right_boundary = 1700

    def __init__(self):

        pygame.init()
        self.balloons_count = 4  # Only one balloon is available at a time, it's the different colors.
        self.balloon_images = ['SCORE/blue.png', 'SCORE/green.png', 'SCORE/red.png', 'SCORE/purple.png']
        self.pop_images = ['SCORE/blue_pop.png', 'SCORE/green_pop.png', 'SCORE/red_pop.png', 'SCORE/purple_pop.png']
        self.balloon_size = (200, 250)
        self.pop_size = (100, 70)
        self.x_pos = random.randint(self.left_boundary, self.right_boundary)
        self.y_pos = (self.disp_height * 1)
        self.y_change = -20  # Pixels moved per refresh.
        self.score = 0
        self.quit_game = False
        self.time_limit = True
        self.time_elapsed = 0
        self.timer_max = 30
        self.clock = pygame.time.Clock()
        self.clock.tick(60)
        self.game_speed = 0  # FIXME: We need to add a speed feature.
        self.restart_game = False

        #  Screen Startup
        self.gameDisplay = pygame.display.set_mode((self.disp_width, self.disp_height))
        pygame.display.set_caption("Balloons")  # See, I didn't change the name.
        self.gameDisplay.fill(BLACK)  # REDUNDANT

        self.font = pygame.font.SysFont('Arial', 50)
        self.font2 = pygame.font.SysFont('Arial', 40)
        self.game_over_font = pygame.font.SysFont('Arial', 90, bold=True)
        self.results_font = pygame.font.SysFont('Arial', 60)

        img = self.font2.render(f'Follow Calibration Instructions in Terminal', True, (255, 255, 255))
        self.gameDisplay.blit(img, (self.disp_width/2 - 400, self.disp_height/2))
        pygame.draw.circle(self.gameDisplay, (0, 255, 0), [0, 0], 25, 25)
        pygame.draw.circle(self.gameDisplay, (0, 255, 0), [0, self.disp_height], 25, 25)
        pygame.draw.circle(self.gameDisplay, (0, 255, 0), [self.disp_width, 0], 25, 25)
        pygame.draw.circle(self.gameDisplay, (0, 255, 0), [self.disp_width, self.disp_height], 25, 25)
        pygame.display.update()

    def game_begin(self):
        # Creates a blank screen, and records a start time.
        self.gameDisplay.fill(WHITE)
        self.start_time = time.time()   # WHOLE METHOD WILL BE REMOVED.

    def update_score(self):

        img = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        self.gameDisplay.blit(img, (30, 30))

    def update_timer(self):

        time_left = round(self.timer_max - self.time_elapsed, 2)
        img = self.font.render(f'Time Left: {time_left}', True, (0, 0, 0))
        self.gameDisplay.blit(img, ((self.disp_width - 375), 30))

    def display(self, x, y):

        # Loads the appropriate balloon image.
        current_index = self.balloons_count % len(self.balloon_images)
        image = pygame.image.load(self.balloon_images[current_index])
        image = pygame.transform.scale(image, self.balloon_size)
        self.gameDisplay.blit(image, (x, y))

    def step(self):

        self.y_pos += self.y_change
        #  Change Position.
        if self.y_pos <= -200:
            self.x_pos = random.randint(self.left_boundary, self.right_boundary)
            self.y_pos = (self.disp_height * 1)
            self.balloons_count += 1
        #  Update frame.
        self.gameDisplay.fill(WHITE)
        self.display(self.x_pos, self.y_pos)
        self.update_score()
        current_time = time.time()
        self.time_elapsed = current_time - self.start_time
        self.update_timer()
        pygame.display.update()

        if (self.time_elapsed >= self.timer_max) and self.time_limit:
            self.game_over()

    def pop(self):

        start_time = time.time()
        elapsed_time = 0

        # For 1.5 seconds.
        while elapsed_time < 1.5:
            self.gameDisplay.fill(WHITE)
            current_image = self.balloons_count % len(self.pop_images)
            image = pygame.image.load(self.pop_images[current_image])
            image = pygame.transform.scale(image, self.pop_size)
            self.gameDisplay.blit(image, (self.x_pos, self.y_pos))
            pygame.display.update()
            elapsed_time = time.time() - start_time

        self.score += 1
        self.y_pos = -500  # THIS IS SO THAT THE GAME UPDATES TO A NEW BALLOON.

    def game_over(self):

        # Previous Code.
        self.gameDisplay.fill(WHITE)
        game_over = self.game_over_font.render(f'Game Over!', True, (255, 0, 0))
        self.gameDisplay.blit(game_over, ((self.disp_width/2 - 265), (self.disp_height/2 - 100)))
        results = self.results_font.render(f'You hit {self.score} balloons!', True, (0, 0, 0))
        self.gameDisplay.blit(results, (self.disp_width/2 - 245, self.disp_height/2))
        pygame.display.update()

        if input("Play again?") == "Yes":
            self.restart_game = True
            self.quit_game = False
        else:
            self.quit_game = True

