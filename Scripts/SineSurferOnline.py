"""

SineSurfer!

SineSurferOnline.py:

Client-side script for running the game. 
Will interact with SineServer.py.

---------

Game made for CENG356 - Engineering System Software
Uses Pygame fo rgame logic + rendering, sockets for network communications.
Launch SineServer.py before launching instances of SineSurfer.py

--------

To do: (optional)

Ping server to account for latency in local ball2 position
new graphics?
Tkinter GUI for hosting / joining game sessions
Gracefully exit game / r to restart?

"""

import pygame
import math
import sys
import random
from socket import *
from pygame.locals import *
from time import *

# Start Pygame instance
pygame.init()


# Global controls + Variables: -------------

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 40)
SERVER_PORT = 9000

#framecount = 0

#-------------------------------------------


s = socket(AF_INET, SOCK_STREAM)
s.connect(("", SERVER_PORT))


# Class Definitions -------------------------------------------

class BallSprite(pygame.sprite.Sprite):

	
	def __init__(self, image, position):					# Initialize player with intitial conditions.
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.image = self.src_image
		self.rect = self.image.get_rect()
		self.position = position
		self.speed = 0
		self.k_up = self.k_down = self.k_left = self.k_right =  0
		self.path = [(296, 352), (292, 356)]

	def update(self, deltat, screen, number, online_pos=None):				# Calculate new position of the ball

		x, y = self.position

		if(online_pos != None):
			if(math.fabs(online_pos) < 9000):
				if online_pos > 0: 		# filter erroneous positions, will maintain previous value of y
					y = online_pos
		
		else:
			x, y = self.position
			self.speed += (self.k_up + self.k_down)
			if y > 300:
				self.speed -= 2
			elif y <= 300:
				self.speed += 2
			if self.speed < -23:
				self.speed = -23
			elif self.speed > 23:
				self.speed = 23
			y += self.speed

		# Draw trace of player's position history:
		if self.alive():
			pygame.draw.lines(screen, ((math.cos(math.radians(number / 2)) * 122) + 122, 255,(math.cos(math.radians(number / 6)) * 122) + 122), False, self.path, 3)  
			
		for i,e in enumerate(self.path):		# move each point in path array back.
			a = self.path[i][0]
			b = self.path[i][1]
			a -= 4
			self.path[i] = (a, b)

		self.position = (x, y)						
		self.path.append(tuple([x, y]))		# add current position to path array		
		self.rect = self.image.get_rect()
		if(y < 9000):				# DEBUG
			self.rect.center = (x,y)		
		if len(self.path) > 75:
			del self.path[0]		# trim path array.

		# Send position to server	
		if (online_pos is None): 
			s.send(str(y).encode('utf-8'))  	
			
		
class BarSprite(pygame.sprite.Sprite):			# obstacles.

	def __init__(self, position):
		score = 0
		pygame.sprite.Sprite.__init__(self)
		self.is_hit = False
		self.image = pygame.image.load('sprites/Bar2.png')
		self.rect = self.image.get_rect()
		self.position = position

	def update(self, hits):
		x, y = self.position
		x -= 4						# this should be changed to 4 once update is called once / frame.
		if x < -100:
			x = 1100
			y = random.randint(80, 600)
			self.is_hit = False
		self.position = (x, y)	
		if self in hits or self.is_hit == True:
			self.image = pygame.image.load('sprites/bar_hit.png')
			self.is_hit = True	
		elif self.is_hit == False:
			self.image = pygame.image.load('sprites/Bar2.png')
			self.is_hit = False
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		
	
# ----------------------------------------------------------------


def start_game():	
	
	while(True):
		seed = s.recv(4096)
		print(seed)
		try:
			if int(seed) > 0: break
		except:
			pass

	print("recieved seed {}".format(int(seed)))

	# Seed RNG

	random.seed(int(seed))

	# Initialize game state with bar positions
	
	bars = [
		BarSprite((1100, random.randint(80, 600))),
		BarSprite((1300, random.randint(80, 600))),
		BarSprite((1500, random.randint(80, 600))),
		BarSprite((1700, random.randint(80, 600))),
		BarSprite((1900, random.randint(80, 600))),
		BarSprite((2100, random.randint(80, 600)))
	]

	bar_group = pygame.sprite.RenderPlain(*bars)

	# Initialize Balls

	ball = BallSprite('sprites/ball.png', (300, 350))

	# make separate group for player 2 so they can be updated separately.

	ball2 = BallSprite('sprites/ball2.png', (300, 350))  # TO DO: make x coord proportional to ping / latency

	ball_group = pygame.sprite.RenderPlain(ball, ball2)
	background = pygame.image.load('sprites/background.png')
	screen.blit(background, (0,0))

	first_frame = True		# Mystery bug: game won't work without this
	score = 0
	game_time = 0
	game_over = False

	# 3-2-1 countdown sequence. ------------------ ---------

	while(True):

		try: 
			count = int(s.recv(4096))
		except:
			count = 4
		
		if((count != 0) & (count < 6)): 
			print(count)
			text = font.render(str(count), True, (255, 255, 255))	# place text on screen	
			screen.blit(background, (0,0))
			screen.blit(text, (320, 300))
			pygame.display.flip()

		if(count == 1):
			sleep(1)
			break			

	s.setblocking(0)		# Set socket to non-blocking (can return nothing)
		
	print("finished countdown")

	# End countdown, enter gameplay loop ---------------------

	# Repeating game loop

	winner = 0 # Variable used for keeping track of first player to lose.

	while True:

		deltat = clock.tick(30)

		# get player 2's position.

		try:
			y_coord = int(s.recv(4096))
		except:
			y_coord = 9000    # ignore value used as in if y_coord == 9000: ignore. 


		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN

			if event.key == K_UP: ball.k_up = down * -1
			elif event.key == K_DOWN: ball.k_down = down * 1		
			elif event.key == K_ESCAPE: 

				sys.exit()
			elif event.key == K_r: start_game()
			
		if not first_frame:																	# Mystery bug
			hits = pygame.sprite.groupcollide(bar_group, ball_group, False, True)
		else: 
			hits = ()	
											
		bar_group.update(hits)			 

		if bool(ball_group): game_time += 1  # If at least one ball is still in play
		score =  (game_time - 170) / 50		# Calculating score based on time  
		if score < 0: score = 0			# score can't be negative
		
		if ball.alive() and not ball2.alive() and winner == 0:
			winner = 1

		if ball2.alive() and not ball.alive() and winner == 0:
			winner = 2		


		if bool(ball_group):
			score = ("Score: %.0f" % score)
		else:
			if winner == 1:
				score = ("You Win!   Final Score = %.0f        Press R to Restart" % score)
			elif winner == 2:
				score = ("You Lose!   Final Score = %.0f        Press R to Restart" % score)
			
		text = font.render(score, True, (255, 255, 255))	# place text on screen	
		screen.blit(background, (0,0))					    # clear screen

		if bool(ball):								# update only if the player still exists
			ball.update(deltat, screen, game_time)
#			ball.draw(screen)

		if  bool(ball2):								#  Update ball if player 2 is not dead
			ball2.update(deltat, screen, game_time, y_coord)
#			ball2.draw()

		bar_group.draw(screen)								# render bars
		ball_group.draw(screen)	
#		ball2_group.draw(screen)							# render balls
		screen.blit(text, (20, 540))
		pygame.display.flip()								# this is necessary otherwise nothing displays

		first_frame = False


		
start_game()	
		
		
		