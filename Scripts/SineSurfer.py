import pygame
import math
import sys
import random
from pgu import high

from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 40)

random.seed()

highscores= high.High('scores.txt', 20)


class BallSprite(pygame.sprite.Sprite):

	
	def __init__(self, image, position):
		pygame.sprite.Sprite.__init__(self)
		self.src_image = pygame.image.load(image)
		self.image = self.src_image
		self.rect = self.image.get_rect()
		self.position = position
		self.speed = 0
		self.k_up = self.k_down = self.k_left = self.k_right =  0
		self.path = [(296, 352), (292, 356)]

	def update(self, deltat, screen, number):
#		print(self.path)
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
		
#		print((math.cos(math.radians(number))) * 122 + 122)

		pygame.draw.lines(screen, ((math.cos(math.radians(number / 2)) * 122) + 122, 255,(math.cos(math.radians(number / 6)) * 122) + 122), False, self.path, 3)
			
		for i,e in enumerate(self.path):
			a = self.path[i][0]
			b = self.path[i][1]
			a -= 4
			self.path[i] = (a, b)
			
		self.position = (x, y)
		self.path.append(tuple([x, y]))
		self.image = self.src_image
		self.rect = self.image.get_rect()
		self.rect.center = self.position		
		if len(self.path) > 75:
			del self.path[0]
			
			
		
class BarSprite(pygame.sprite.Sprite):

	def __init__(self, position):
		score = 0
		pygame.sprite.Sprite.__init__(self)
		self.is_hit = False
		self.image = pygame.image.load('sprites/Bar2.png')
		self.rect = self.image.get_rect()
		self.position = position

	def update(self, hits):
		x, y = self.position
		x -= 4
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
		
	



def start_game():
	
	bars = [
		BarSprite((1100, random.randint(80, 600))),
		BarSprite((1300, random.randint(80, 600))),
		BarSprite((1500, random.randint(80, 600))),
		BarSprite((1700, random.randint(80, 600))),
		BarSprite((1900, random.randint(80, 600))),
		BarSprite((2100, random.randint(80, 600)))
	]
	bar_group = pygame.sprite.RenderPlain(*bars)
	ball = BallSprite('sprites/ball.png', (300, 350))
	ball_group = pygame.sprite.RenderPlain(ball)
	background = pygame.image.load('sprites/background.png')
	screen.blit(background, (0,0))

	first_frame = True		#I know this a weak workaround for a fixable bug, but what can you do?
	score = 0
	time = 0
	game_over = False
		
	while True:

		deltat = clock.tick(30)
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN
			if event.key == K_UP: ball.k_up = down * -1
			elif event.key == K_DOWN: ball.k_down = down * 1		
			elif event.key == K_ESCAPE: 
				highscores.save()
				sys.exit()
			elif event.key == K_r: start_game()
			
		if not first_frame:																	#I have no idea why this is necessary
			hits = pygame.sprite.groupcollide(bar_group, ball_group, False, True)			
		else: hits = ()	

		bar_group.update(hits)

		if bool(ball_group): time += 1
		score =  (time - 170) / 50
		if score < 0: score = 0
		points = score
		
		if bool(ball_group):
			score = ("Score: %.0f" % score)
		else:
			score = ("Game over!   Final Score = %.0f        Press R to Restart" % score)
			
		text = font.render(score, True, (255, 255, 255))
		screen.blit(background, (0,0))					    #clear screen
		
		ball_group.update(deltat, screen, time)
		bar_group.draw(screen)
		ball_group.draw(screen)
		screen.blit(text, (20, 540))
		pygame.display.flip()
		first_frame = False

	
		
start_game()	
		
		
		