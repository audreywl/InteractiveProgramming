"""This is Katie and Audrey's Software Design Mini-Project 4. It uses pygame to load a music visualizer that you can jump on"""
import pygame
from pygame.locals import QUIT, KEYDOWN #our only controller should be the keyboard (and music) so no need to import mouse stuff
import time
from random import choice
inp = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK,0)

f = open('song_values.pickle','r')
music_heights = pickle.load(f)
f.close()
print music_heights

class PygameView(object):
    """ Visualizes the music game in a pygame window """
    def __init__(self, model, screen):
        """ Initialize the view with the specified model
            and screen. """
        self.model = model
        self.screen = screen

    def draw(self):
        """ Draw the game state to the screen """
        self.screen.fill(pygame.Color('black')) #have a black background
        #TODO:draw music bars
        for bar in self.model.bars:
            r = pygame.Rect(bar.left, bar.top, bar.width, bar.height)
            pygame.draw.rect(self.screen, pygame.Color(bar.color), g)

        #draw the character to the screen
        r = pygame.Rect(self.model.character.left,
                        self.model.character.top,
                        self.model.character.width,
                        self.model.character.height)
        pygame.draw.rect(self.screen, pygame.Color('white'), r)
        pygame.display.update()

class Bar(object):
    """A single vertical rectangle in the music visualizer"""
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class Character(object):
    """ Our little main character (also a rectanlge) """
    def __init__(self, left, top, width, height):
        """ Initialize our character """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class MusicGameModel(object):
    """ Stores the game state for our visualizer game """
    def __init__(self):
        self.bars = music_heights
        self.MARGIN = 5
        self.BAR_WIDTH = 20
        for i in music_heights:
            lc = (self.MARGIN)
            for height in i:
                self.BAR_HEIGHT = height
                tc = 480 - height 
                bar = Bar(lc, tc, self.BAR_WIDTH, self.BAR_HEIGHT)
                lc += self.BAR_WIDTH + self.MARGIN
        self.bars.append(bar)
        self.character = Character(self.MARGIN, self.MARGIN + 20, 50, 20)

    # def __init__(self):
    #   self.bars = []
    #   self.MARGIN = 5

    # #TODO: Implement bars initialization

    #   for new in range(song_values[]):
    #       new_bar = Bar(5, 5, 20, song_values[0[]])
    #       self.bars.append(new_bar)
    #       for left in range(self.MARGIN,
    #                         640 - self.BAR_WIDTH - self.MARGIN,
    #                         self.BAR_WIDTH + self.MARGIN):
    #           for top in range(self.MARGIN,
    #                            480/3 + self.BAR_HEIGHT + self.MARGIN):
    #               brick = Bar(left, top, self.BAR_WIDTH, self.BRICK_HEIGHT)
    #               self.bricks.append(brick)

    #TODO: Implement character initialization
        # self.paddle = Paddle(640/2, 480 - 30, 50, 20)


class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Look for keypresses to
            modify the x adn y positions of the character"""
        pygame.set_repeat(10,10)
        if event.type == KEYUP:
        #TODO: Modify character left and top based on keypress
            #RESEARCH: is possible for length of keypress to modify height of jump?
            if event.key == pygame.K_LEFT:
                self.model.character.left -= 10
            elif event.key == pygame.K_RIGHT:
                self.model.character.left += 10
            if event.key = K_UP:
                self.model.character.top += 10
        elif event.type == KEYDOWN
            if event.key == pygame.K_UP:
                if 
        # pygame.set_repeat() -> None
        # pygame.set_repeat(delay, interval) -> None
        # get_repeat() -> (delay, interval)

        # if e.type == KEYDOWN:
        #         if e.key == K_LEFT:
        #             ship.xspeed -= SPEED
        #         elif e.key == K_RIGHT:
        #             ship.xspeed += SPEED
        #         elif e.key == K_UP:
        #             ship.yspeed -= SPEED
        #         elif e.key == K_DOWN:
        #             ship.yspeed += SPEED
        #         elif e.key == K_SPACE
        #             ship.firing = True
        #     elif e.type == KEYUP:
        #         if e.key == K_LEFT:
        #             ship.xspeed += SPEED
        #         elif e.key == K_RIGHT:
        #             ship.xspeed -= SPEED
        #         elif e.key == K_UP:
        #             ship.yspeed += SPEED
        #         elif e.key == K_DOWN:
        #             ship.yspeed -= SPEED
        #         elif e.key == K_SPACE:
        #             ship.firing == False



if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)
    model = MusicGameModel()
    view = PygameView(model, screen)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
        time.sleep(.001)
