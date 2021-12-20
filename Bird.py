import pygame, sys
from Drawing import Drawing

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

bird_pics = [
	[
		pygame.image.load("content/redbird-up.png"),
		pygame.image.load("content/redbird-mid.png"),
		pygame.image.load("content/redbird-down.png")
	],
	[
		pygame.image.load("content/bluebird-up.png"),
		pygame.image.load("content/bluebird-mid.png"),
		pygame.image.load("content/bluebird-down.png")
	],
	[
		pygame.image.load("content/yellowbird-up.png"),
		pygame.image.load("content/yellowbird-mid.png"),
		pygame.image.load("content/yellowbird-down.png")
	]
]

flap_rotate = [0, 0, 0, 1, 1, 1, 2, 2, 2] # Required in affect after bird rotation


class Bird(pygame.sprite.Sprite):
	def __init__(self, bird_index):
		pygame.sprite.Sprite.__init__(self)
		self.bird_index = bird_index
		self.x=0; self.y=0; self.obj_y=0
		self.x = int(SCREEN_WIDTH * 0.2)
		self.y = int((SCREEN_HEIGHT - bird_pics[0][0].get_height()) / 2)
		self.rotation = 0
		self.jumped = False
		self.flap = 0
#		print(self.y); sys.exit(0)
		self.obj_y = self.y - 50

		self.endOfLife = False
		self.image = bird_pics[self.bird_index][1]
		self.surface = pygame.surface.Surface((288, 512), pygame.SRCALPHA)
		self.rect = self.surface.get_rect()
		self.mask = pygame.mask.from_surface(self.surface)

	def set_x_coord (self, val):
		self.x = val

	def get_x_coord(self):
		return self.x

	def set_y_coord (self, val):
		self.y = val

	def get_y_coord(self):
		return self.y


	def draw(self, screen):
		Drawing.__init__(screen)
		self.surface.fill((0, 0, 0, 0))

		if self.jumped:
			self.image = pygame.transform.rotate(bird_pics[self.bird_index][0], self.rotation)
			self.surface.blit(self.image, (self.x, self.y))
		else:
			self.image = pygame.transform.rotate(bird_pics[self.bird_index][flap_rotate[self.flap]], self.rotation)
			self.surface.blit(self.image, (self.x, self.y))

		self.image = self.surface
		self.mask = pygame.mask.from_surface(self.surface)
		screen.blit(self.surface, (self.surface.get_rect().x, self.surface.get_rect().y))

	def jump(self):
		self.jumped = True
		self.rotation = 25

		self.obj_y = self.y - 40

		self.update()

	def update(self):
		self.flap = (self.flap + 1) % len(flap_rotate)
		if self.endOfLife:
			self.dead()
		else:
			if not self.jumped and (not self.rotation <= -90) and (not self.endOfLife):
				self.rotation -= int(2 + abs(0.15 * self.rotation))
			if self.jumped and (not self.y == self.obj_y) and (not self.endOfLife):
				self.y -= 7
			if self.jumped and self.y <= self.obj_y and (not self.endOfLife):
				self.jumped = False

			if self.rotation < 5 and not self.jumped and not self.endOfLife:
				self.y += int(5 + 0.15 * abs(self.rotation))

		self.rect = self.surface.get_rect()

	def dead(self):
		self.flap = 5
		if self.rotation > -90:
			self.rotation -= int(5 + abs(0.1 * self.rotation))
		if self.y <= 370:
			self.y += int(8 + 0.15 * abs(self.rotation))
