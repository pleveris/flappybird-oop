import random

import pygame

PIPE_GAP = 100
MIN_Y = 400

PIPE_HEIGHT = 320
PIPE_WIDTH = 50

PLAYING_FIELD = 400

PIPE_IMAGES = [
	[
		pygame.image.load("content/lower.png"),
		pygame.transform.rotate(pygame.image.load("content/lower.png"), 180)
	],
	[
		pygame.image.load("content/upper.png"),
		pygame.transform.rotate(pygame.image.load("content/upper.png"), 180)
	]
]

PIPE_LOWER = random.randrange(PIPE_GAP + 30, MIN_Y - 30)
PIPE_UPPER = PIPE_LOWER - PIPE_GAP - PIPE_HEIGHT


class LowerPipe(pygame.sprite.Sprite):
	def __init__(self, index=0):
		pygame.sprite.Sprite.__init__(self)

		self.index = index

		self.x = 298
		self.y = PIPE_LOWER

		self.x_vel = -3

		self.image = PIPE_IMAGES[self.index][0]
		self.surface = pygame.surface.Surface((288, 512), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.mask = pygame.mask.from_surface(self.surface)

	def draw(self, output):
		self.surface.fill((0, 0, 0, 0))
		self.image = PIPE_IMAGES[self.index][0]
		self.surface.blit(self.image, (self.x, self.y))

		self.image = self.surface
		self.mask = pygame.mask.from_surface(self.surface)
		output.blit(self.surface, (self.surface.get_rect().x, self.surface.get_rect().y))

	def update(self):
		self.x += self.x_vel


class UpperPipe(pygame.sprite.Sprite):
	def __init__(self, index=1):
		pygame.sprite.Sprite.__init__(self)

		self.index = index

		self.x = 298
		self.y = PIPE_UPPER

		self.x_vel = -3

		self.image = PIPE_IMAGES[self.index][1]
		self.surface = pygame.surface.Surface((288, 512), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.mask = pygame.mask.from_surface(self.surface)

	def draw(self, output):
		self.surface.fill((0, 0, 0, 0))
		self.image = PIPE_IMAGES[self.index][1]
		self.surface.blit(self.image, (self.x, self.y))

		self.image = self.surface
		self.mask = pygame.mask.from_surface(self.surface)
		output.blit(self.surface, (self.surface.get_rect().x, self.surface.get_rect().y))

	def update(self):
		self.x += self.x_vel
