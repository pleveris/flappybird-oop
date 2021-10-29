"""
FlappyBird OOP game, made as a Course Project for Software Engineering Design course at VilniusTech.
Copyright(C) Paulius Leveris 2021
(part 1 of 2)
"""


import random
import sys

import pygame
from pygame.locals import *

import Bird
import Pipe

pygame.init()

WIDTH = 288
HEIGHT = 512

FPS = 30
CLOCK = pygame.time.Clock()

output = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird OOP game")
pygame.display.set_icon(pygame.image.load('game.ico'))

game_back = [pygame.image.load("content/bg.png")]

digits = [pygame.image.load('content/0.png'),
		  pygame.image.load('content/1.png'),
		  pygame.image.load('content/2.png'),
		  pygame.image.load('content/3.png'),
		  pygame.image.load('content/4.png'),
		  pygame.image.load('content/5.png'),
		  pygame.image.load('content/6.png'),
		  pygame.image.load('content/7.png'),
		  pygame.image.load('content/8.png'),
		  pygame.image.load('content/9.png')]

SCORE = 0

SOUNDS = {
	'die': pygame.mixer.Sound('content/die.wav'),
	'hit': pygame.mixer.Sound('content/hit.wav'),
	'point': pygame.mixer.Sound('content/point.wav'),
	'wing': pygame.mixer.Sound('content/wing.wav')
}


def getPipesReady():
	lower_new_pipe_1 = Pipe.LowerPipe()
	upper_new_pipe_1 = Pipe.UpperPipe()

	Pipe.PIPE_LOWER = random.randrange(Pipe.PIPE_GAP + 30, Pipe.MIN_Y - 30)
	Pipe.PIPE_UPPER = Pipe.PIPE_LOWER - Pipe.PIPE_GAP - Pipe.PIPE_HEIGHT

	lower_new_pipe_2 = Pipe.LowerPipe()
	lower_new_pipe_2.x += (WIDTH * 0.5)

	global lower_pipe_list
	lower_pipe_list = [lower_new_pipe_1, lower_new_pipe_2]

	upper_new_pipe_2 = Pipe.UpperPipe()
	upper_new_pipe_2.x += (WIDTH * 0.5)

	global upper_pipe_list
	upper_pipe_list = [upper_new_pipe_1, upper_new_pipe_2]


def generateBackground():
	global background
	background = game_back


def setupBirds():
	global bird_ind
	bird_ind = random.randrange(0, 3)

	global bird
	bird = Bird.Bird(bird_ind)

def remapObjsOnScreen():
	output.blit(random.choice(background), (0, 0))

	for pipe in lower_pipe_list:
		pipe.draw(output)

	for pipe in upper_pipe_list:
		pipe.draw(output)

	bird.draw(output)
	show_score(SCORE)

	pygame.display.update()


def show_score(score):
	score_digits = [int(x) for x in list(str(score))]
	total_width = 0

	for digit in score_digits:
		total_width += digits[digit].get_width()

	x_offset = (WIDTH - total_width) / 2

	for digit in score_digits:
		output.blit(digits[digit], (x_offset, HEIGHT * 0.1))
		x_offset += digits[digit].get_width()


# --------- UPDATER FUNCTIONS ---------

def update_pipe_list():
	Pipe.PIPE_LOWER = random.randrange(Pipe.PIPE_GAP + 30, Pipe.MIN_Y - 30)
	Pipe.PIPE_UPPER = Pipe.PIPE_LOWER - Pipe.PIPE_GAP - Pipe.PIPE_HEIGHT

	if 0 < lower_pipe_list[0].x < 3:
		new_pipe = Pipe.LowerPipe(pipe_col)
		lower_pipe_list.append(new_pipe)

	if lower_pipe_list[0].x < 0 - Pipe.PIPE_WIDTH:
		lower_pipe_list.pop(0)

	if 0 < upper_pipe_list[0].x < 3:
		new_pipe = Pipe.UpperPipe(pipe_col)
		upper_pipe_list.append(new_pipe)

	if upper_pipe_list[0].x < 0 - Pipe.PIPE_WIDTH:
		upper_pipe_list.pop(0)

# What if collision is found?

def detect_collision():
	if (bird.y + Bird.bird_pics[0][1].get_height()) >= 400 - 5:
		if not bird.endOfLife:
			SOUNDS['hit'].play()
		bird.endOfLife = True
		return True
	else:
		for upper_pipe, lower_pipe in zip(upper_pipe_list, lower_pipe_list):
			if (pygame.sprite.collide_mask(bird, upper_pipe) is not None) or \
					(pygame.sprite.collide_mask(bird, lower_pipe) is not None):
				if not bird.endOfLife:
					SOUNDS['hit'].play()
					SOUNDS['die'].play()
				bird.endOfLife = True
				return True
	return False


def check_for_score():
	player_mid_pos = bird.x + Bird.bird_pics[0][1].get_width() / 2

	for pipe in upper_pipe_list:
		pipe_mid_pos = pipe.x + Pipe.PIPE_IMAGES[0][0].get_width() / 2
		if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4 and not bird.endOfLife:
			global SCORE
			SCORE += 1
			SOUNDS['point'].play()

# --------- MAIN GAME FUNCTIONS ---------


def start():
	generateBackground()
	setupBirds()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE): return

		output.blit(random.choice(background), (0, 0))
		bird.draw(output)
		bird.update()
		pygame.display.update()
		CLOCK.tick(FPS)


def main_loop():
	global SCORE
	SCORE = 0

	start()
	getPipesReady()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif (event.type == MOUSEBUTTONDOWN or (event.type == KEYDOWN and
														(event.key == K_UP or event.key == K_SPACE))) and \
					(not bird.y <= 0) and not bird.endOfLife:
				bird.jump()
				SOUNDS['wing'].play()

			elif bird.endOfLife and (event.type == KEYDOWN and (event.key == K_UP or event.key == K_SPACE) or
											 event.type == MOUSEBUTTONDOWN):
				main_loop()

		update_pipe_list()
		check_for_score()

		for pipe in lower_pipe_list:
			pipe.update()

		for pipe in upper_pipe_list:
			pipe.update()

		bird.update()

		if detect_collision():
			for upper_pipe, lower_pipe in zip(upper_pipe_list, lower_pipe_list):
				upper_pipe.x_vel = 0
				lower_pipe.x_vel = 0

		remapObjsOnScreen()

		CLOCK.tick(FPS)


main_loop()  # GAME INITIALIZER
