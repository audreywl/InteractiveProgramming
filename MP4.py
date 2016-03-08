"""This is Katie and Audrey's Software Design Mini-Project 4. It uses pygame to load a music visualizer that you can jump on"""
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP #our only controller should be the keyboard (and music) so no need to import mouse stuff
import time
from random import choice
import alsaaudio as aa
import audioop
import pickle
import math
import numpy as np
from struct import unpack


def calculate_levels(data, chunk,sample_rate):
	"""This code, which we got from somebody else's project at https://www.raspberrypi.org/forums/viewtopic.php?p=314087, performs a fourier transform on the incoming audio stream, finding the amplitudes of 16 frequencies"""
	# Convert raw data to numpy array
	data = unpack("%dh"%(len(data)/2),data)
	data = np.array(data, dtype='h')
	# Apply FFT - real data so rfft used
	fourier=np.fft.rfft(data)
	# Remove last element in array to make it the same size as chunk
	fourier=np.delete(fourier,len(fourier)-1)
	# Find amplitude
	power = np.log10(np.abs(fourier))**2
	# Arrange array into 16 rows
	power = np.reshape(power,(16,chunk/16))
	matrix= (np.average(power, axis=1))
	#This was part of testing how the music affected the transform by displaying it in the command line
	#pretty_matrix = np.int_(matrix)
	#print pretty_matrix
	#Convert out of the weird numpy types
	matrix=matrix.tolist()
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
		#draw the music bars to the screen
		for bar in self.model.bars:
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
		self.color = 'red' #TODO: make this more interesting colors

class Character(object):
	""" Our little main character (also a rectanlge) """
	def __init__(self, left, top, width, height):
		""" Initialize our character """
		self.left = left
		self.top = top
		self.width = width
		self.height = height
		self.bottom = self.top+self.height
		self.vx = 0 #horizontal velocity
		self.vy = 0 #vertical velocity
		self.a = -10 #acceleration

	


class MusicGameModel(object):
	""" Stores the game state for our visualizer game """
	def __init__(self):
		#Initialize bars
		self.bars = []
		self.pybars = []
		self.MARGIN = 3
		self.BAR_WIDTH = 20
		self.BAR_HEIGHT = 20
		lc = self.MARGIN
		for i in range(0,16):
			tc = 480-self.BAR_HEIGHT
			bar = Bar(lc, tc, self.BAR_WIDTH, self.BAR_HEIGHT)
			lc += self.BAR_HEIGHT + self.MARGIN +self.BAR_WIDTH
			self.bars.append(bar)
		#initialize character
		self.character = Character(self.MARGIN, self.MARGIN + 20, 20, 50)
		self.pychar = pygame.Rect(self.character.left, self.character.top, self.character.width, self.character.height)
		#Turn stuff into actual pygame objects
		for bar in self.bars:
			r = pygame.Rect(bar.left, bar.top, bar.width, bar.height)
			self.pybars.append(r)

	def update_physics(self, vx=0, vy=0):
		"""Adjust position and velocity"""
		self.character.vx = vx
		self.character.vy = vy - self.character.a
		self.character.left += self.character.vx
		self.character.top += self.character.vy
		self.character.bottom = self.character.top+self.character.height
		#checks for collisions with the bottom of the screen
		if self.character.bottom > 480:
			self.character.top = 480-self.character.height
		#TODO: check for collisions with the music bars
	#TODO: Maybe update_physics, and the collision code, should be down here?

	def detect_collisions(self):
		"""checks if there are collisions with anything. If so, moves the character up out of the way"""
		self.pychar = pygame.Rect(self.character.left, self.character.top, self.character.width, self.character.height)
		#Turn stuff into actual pygame objects
		for bar in self.bars:
			r = pygame.Rect(bar.left, bar.top, bar.width, bar.height)
			self.pybars.append(r)
		for bar in self.pybars:
			#check if the bar and character are colliding
			if bar.colliderect(self.pychar):
				#check if it approached from the top (the top row of the bar is inside character rectangle)
				for point in range(bar.left,bar.left+bar.width):
					if bar.collidepoint:
						self.character.top -=10
						break
						print 'COLLISION'


class PyGameKeyboardController(object):
	def __init__(self, model):
		self.model = model
		pygame.key.set_repeat(10,20)

	def handle_event(self, event):
		""" Look for keypresses to
			modify the x adn y positions of the character"""
		if event.type == KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.model.update_physics(-10)
			elif event.key == pygame.K_RIGHT:
				self.model.update_physics(10)
			if event.key == pygame.K_UP:
				self.model.update_physics(0,-60)
		# pygame.set_repeat() -> None
		# pygame.set_repeat(delay, interval) -> None
		# get_repeat() -> (delay, interval)


class MusicController(object):
	def __init__(self, model):
		self.model = model

	def adjust_bars(self, music_chunk):
		"""Changes the bars heights in the model based on the current values for music"""
		for i in range(len(music_chunk)):
			bars_list=self.model.bars
			current_bar=bars_list[i]
			current_bar.height=400-20*music_chunk[i]
			current_bar.top=480-current_bar.height


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
		model.update_physics()
		model.detect_collisions()
		#Quit Game
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
				current_levels=calculate_levels(data, chunk, sample_rate)
				music.adjust_bars(current_levels)
			except audioop.error, e:
				if e.message !="not a whole number of frames":
					raise e
		view.draw()
		time.sleep(.09)
		data_in.pause(0)
