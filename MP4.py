"""This is Katie and Audrey's Software Design Mini-Project 4. It uses pygame to load a music visualizer that you can jump on"""
import pygame
from pygame.locals import QUIT, KEYDOWN #our only controller should be the keyboard (and music) so no need to import mouse stuff
import time
from random import choice
import alsaaudio
import audioop

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
		# TODO:draw music bars
		# for bar in self.model.bars:
		# 	r = pygame.Rect(brick.left, brick.top, brick.width, brick.height)
		# 	pygame.draw.rect(self.screen, pygame.Color(brick.color), r)

		# draw the character to the screen
		# r = pygame.Rect(self.model.paddle.left,
		# 				self.model.paddle.top,
		# 				self.model.paddle.width,
		# 				self.model.paddle.height)
		# pygame.draw.rect(self.screen, pygame.Color('white'), r)
		# pygame.display.update()

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
		self.bars = []
		self.MARGIN = 5

	#TODO: Implement bars initialization

		# new_brick = Brick(5, 5, 40, 20)
		# self.bricks.append(new_brick)
		# for left in range(self.MARGIN,
		#                   640 - self.BRICK_WIDTH - self.MARGIN,
		#                   self.BRICK_WIDTH + self.MARGIN):
		#     for top in range(self.MARGIN,
		#                      480/2,
		#                      self.BRICK_HEIGHT + self.MARGIN):
		#         brick = Brick(left, top, self.BRICK_WIDTH, self.BRICK_HEIGHT)
		#         self.bricks.append(brick)

	#TODO: Implement character initialization
		# self.paddle = Paddle(640/2, 480 - 30, 50, 20)


class PyGameKeyboardController(object):
	def __init__(self, model):
		self.model = model

	def handle_event(self, event):
		""" Look for keypresses to
			modify the x adn y positions of the character"""
		if event.type != KEYDOWN:
			return
		#TODO: Modify character left and top based on keypress
			#RESEARCH: is possible for length of keypress to modify height of jump?
		# if event.key == pygame.K_LEFT:
		# 	self.model.paddle.left -= 10
		# if event.key == pygame.K_RIGHT:
		# 	self.model.paddle.left += 10


   
inp = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK,0)
inp.setchannels(1)
inp.setrate(16000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(160)
       
while True:
        l,data = inp.read()
        if l:
                print audioop.rms(data,2)


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
>>>>>>> ffdfe7a3b0a155d99eff18304fbc8fc128c3a7e0
