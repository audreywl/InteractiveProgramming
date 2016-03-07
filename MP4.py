"""This is Katie and Audrey's Software Design Mini-Project 4. It uses pygame to load a music visualizer that you can jump on"""
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP #our only controller should be the keyboard (and music) so no need to import mouse stuff
import time
from random import choice
import alsaaudio as aa
import audioop
import pickle
import numpy as np
from struct import unpack
#from load_song_values import calculate_levels
#inp = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK,0)

# f = open('test_song','r')
# music_heights = pickle.load(f)
# f.close()
# print type(music_heights)
# print type(music_heights[0])
# print music_heights

def calculate_levels(data, chunk,sample_rate):
	# Convert raw data to numpy array
	data = unpack("%dh"%(len(data)/2),data)
	data = np.array(data, dtype='h')
	# Apply FFT - real data so rfft used
	fourier=np.fft.rfft(data)
	# Remove last element in array to make it the same size as chunk
	fourier=np.delete(fourier,len(fourier)-1)
	# Find amplitude
	power = np.log10(np.abs(fourier))**2
	# Arrange array into 8 rows for the 8 bars on LED matrix
	power = np.reshape(power,(16,chunk/16))
	matrix= (np.average(power, axis=1))
	pretty_matrix = np.int_(matrix)
	matrix=matrix.tolist()
	#print pretty_matrix
	return matrix

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
			# print bar.left
			# print bar.top
			# print bar.width
			# print bar.height
			r = pygame.Rect(bar.left, bar.top, bar.width, bar.height)
			pygame.draw.rect(self.screen, pygame.Color(bar.color),r)

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
		self.color = 'red'

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
		self.BAR_WIDTH = 20
		self.BAR_HEIGHT = 20
		lc = self.MARGIN
		for i in range(0,16):
			tc = 480-self.BAR_HEIGHT
			bar = Bar(lc, tc, self.BAR_WIDTH, self.BAR_HEIGHT)
			lc += self.BAR_HEIGHT + self.MARGIN +self.BAR_WIDTH
			self.bars.append(bar)
		# for i in music_heights:
		# 	lc = (self.MARGIN)
		# 	for heights in i:
		# 		self.BAR_HEIGHT = heights
		# 		tc = 480 - heights 
		# 		bar = Bar(lc, tc, self.BAR_WIDTH, self.BAR_HEIGHT)
		# 		lc += self.BAR_WIDTH + self.MARGIN
		# 	self.bars.append(bar)
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
		#pygame..set_repeat(10,10)
		if event.type == KEYDOWN:
		#TODO: Modify character left and top based on keypress
			#RESEARCH: is possible for length of keypress to modify height of jump?
			if event.key == pygame.K_LEFT:
				self.model.character.left -= 10
			elif event.key == pygame.K_RIGHT:
				self.model.character.left += 10
			if event.key == pygame.K_DOWN:
				self.model.character.top += 10
		# elif event.type == KEYDOWN:
		#     if event.key == pygame.K_UP:
		#         if 
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
class MusicController(object):
	def __init__(self, model):
		self.model = model

	def adjust_bars(self, music_chunk):
		"""Changes the bars heights in the model based on the current values for music"""
		for i in range(len(music_chunk)):
			bars_list=self.model.bars
			current_bar=bars_list[i]
			current_bar.height=5*music_chunk[i]
			current_bar.top=480-5*music_chunk[i]


if __name__ == '__main__':
	pygame.init()
	size = (640, 480)
	screen = pygame.display.set_mode(size)
	model = MusicGameModel()
	view = PygameView(model, screen)
	controller = PyGameKeyboardController(model)
	music = MusicController(model)
	#Music setup
	sample_rate = 44100
	no_channels = 2
	chunk = 512 # Use a multiple of 8
	data_in = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL)#'front:CARD=PCH,DEV=0'
	data_in.setchannels(no_channels)
	data_in.setrate(sample_rate)
	data_in.setformat(aa.PCM_FORMAT_S16_LE)
	data_in.setperiodsize(chunk)
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			controller.handle_event(event)
		#Music Controls
		l,data = data_in.read()
		data_in.pause(1)
		if l:
		# catch frame error
			try:
				current_levels=calculate_levels(data, chunk,sample_rate)
				music.adjust_bars(current_levels)
			except audioop.error, e:
				if e.message !="not a whole number of frames":
					raise e
		view.draw()
		time.sleep(.05)
		data_in.pause(0)
