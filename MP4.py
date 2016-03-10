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

pygame.font.init
print pygame.font.get_default_font()
print pygame.font.match_font('freesansbold')

class PygameView(object):
	""" Visualizes the music game in a pygame window """
	def __init__(self, model, screen):
		""" Initialize the view with the specified model
			and screen. """
		self.model = model
		self.screen = screen
		self.font = pygame.font.Font("freesansbold.ttf",30)

	def draw(self):
		""" Draw the game state to the screen """
		self.screen.fill(pygame.Color('black')) #have a black background
		#draw the music bars to the screen
		for bar in self.model.bars:
			pygame.draw.rect(self.screen, pygame.Color(bar.color),bar)
		#draw the character to the screen
		pygame.draw.rect(self.screen, pygame.Color('white'), self.model.character)
		pygame.display.update()

	def count(self):
		counter = str(self.model.character.num_count)

		text = self.font.render(counter,True,(255,255,255))
		self.screen.blit(text,(10,10))
		pygame.display.update()


class Bar(pygame.Rect):
	"""A single vertical rectangle in the music visualizer"""
	

	def __init__(self, left, top, width, height):
		self.left = left
		self.top = top
		self.width = width
		self.height = height
		self.color = choice(['red','blue','green','orange','purple']) #TODO: make this more interesting colors

class Character(pygame.Rect):
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
		self.a = -20 #acceleration
		self.on_ground = False
		self.which_bar = None
		self.num_count = 0
		self.is_right = True

	
class MusicGameModel(object):
	""" Stores the game state for our visualizer game """
	def __init__(self):
		#Initialize bars
		self.bars = []
		self.MARGIN = 5
		self.BAR_WIDTH = 50
		self.BAR_HEIGHT = 20
		lc = self.MARGIN
		for i in range(0,16):
			tc = 480-self.BAR_HEIGHT
			bar = Bar(lc, tc, self.BAR_WIDTH, self.BAR_HEIGHT)
			lc += self.MARGIN +self.BAR_WIDTH
			self.bars.append(bar)
		#initialize character
		self.character = Character(self.MARGIN, self.MARGIN + 20, 20, 50)
	
		#Turn stuff into actual pygame objects - MUAHAHAHA INHERITANCE

	def update_physics(self, vx=0, vy=0):
		"""Adjust position and velocity"""
		self.character.vx = vx
		self.character.vy = vy - self.character.a
		self.character.left += self.character.vx
		self.character.top += self.character.vy
		self.character.bottom = self.character.top+self.character.height
		

	def detect_collisions(self):
		"""checks if there are collisions with anything. If so, moves the character up out of the way"""
		# #Turn stuff into actual pygame objects - unnecessary because inheritance!
		for bar in self.bars:
			i = self.bars.index(bar)
			#check if the bar and character are colliding
			if bar.colliderect(self.character):
				#check if it approached from the top (the top row of the bar is inside character rectangle)
				right_point=(bar.left+bar.width+10, bar.top-30)
				left_point=(bar.left, bar.top-30)
				if bar.collidepoint(right_point):
					self.character.move(-5,0)
					#print 'COLLIDE RIGHT'
					break
				if bar.collidepoint(left_point):
					self.character.move(5,0)
					#print 'COLLIDE LEFT'
					break
				for point in range(bar.left,bar.left+bar.width):
					if bar.collidepoint:
						self.character.on_ground = True
						self.character.top -= 1
						self.character.which_bar = self.bars[i]
						#print 'COLLIDE BOTTOM'
						break
		#checks for collisions with the bottom of the screen
		if self.character.bottom > 480:
			self.character.top = 480-self.character.height
			self.character.on_ground = True
		#checks for collisions with the top of the screen
		if self.character.top < 0:
			self.character.top = 0
		#checks for collisions with the left of the screen
		if self.character.left < 0:
			self.character.left = 0
			if not self.character.is_right:
				self.character.num_count+=1
				self.character.is_right = True
		#checks for collisions with the right of the screen
		if self.character.left > 640-self.character.width:
			self.character.left = 640 - self.character.width
			if self.character.is_right:
				self.character.num_count +=1
				self.character.is_right = False

	def jump(self):
		"""Keeps character from jumping in mid-air, and adjust bar-sitting to false"""
		if self.character.on_ground:
			self.update_physics(0,-100)
		else:
			self.update_physics()
		self.character.on_ground = False
		self.character.which_bar = None

	def sit_on_bar(self):
		"""Makes the character sit on the bar when not jumping"""
		if self.character.which_bar != None:
			self.character.top = self.character.which_bar.top - self.character.height - 18


class PyGameKeyboardController(object):
# class PyGameController(object):
	def __init__(self, model):
		self.model = model
		pygame.key.set_repeat(10,20)

	def handle_event(self, event):
		""" Look for keypresses to
			modify the x adn y positions of the character"""
		if event.type == KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.model.update_physics(-10)
				self.model.detect_collisions()
			elif event.key == pygame.K_RIGHT:
				self.model.update_physics(10)
				self.model.detect_collisions()
			if event.key == pygame.K_UP:
				self.model.jump()
				self.model.detect_collisions()

class MusicController(object):
	def __init__(self, model):
		self.model = model

	def adjust_bars(self, music_chunk):
		"""Changes the bars heights in the model based on the current values for music"""
		mc_sum = 0
		for i in range(len(music_chunk[:-1])):
			mc_sum += music_chunk[i+1]
		avg_mc = mc_sum/len(music_chunk[1:-1])

		for i in range(len(music_chunk[:-1])):
			bars_list=self.model.bars
			current_bar=bars_list[i-1]
			current_bar.height=300-100*math.fabs(music_chunk[i]-avg_mc)
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
				model.sit_on_bar()
			except audioop.error, e:
				if e.message !="not a whole number of frames":
					raise e
		model.detect_collisions()
		model.update_physics()
		
		view.draw()
		view.count()
		time.sleep(.1)
		data_in.pause(0)
