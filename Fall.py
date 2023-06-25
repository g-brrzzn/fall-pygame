from random import randint, uniform
import pygame
from pygame.locals import *
from datetime import datetime
import sys
from time import time

pygame.init()
clock = pygame.time.Clock()

fhd = (1920, 1080)
hd = (1280, 720)
d = (800, 600)

WINDOW_SIZE = d
screen = pygame.display.set_mode(WINDOW_SIZE)

font = pygame.font.Font(None, 24)
def text(string, x, y):
    string = str(string)
    info = font.render(string, True, (255, 255, 255))
    screen.blit(info, (x, y))


class Fall:
    def __init__(self, quantidade):
        self.locs = []
        for i in range(quantidade):
            snowloc = [randint(1, WINDOW_SIZE[0] - 1), randint(1, WINDOW_SIZE[1] - 1)]
            self.locs.append(snowloc)

    def update(self, gravity=0.3, wind=0.3):
        for loc in self.locs:
            if gravity > 0: loc[1] += gravity + uniform(0.1, 0.9)
            elif gravity < 0: loc[1] += gravity
            loc[0] += wind

            if gravity < 0 or wind < 0:
                if loc[1] < 0: loc[1] = WINDOW_SIZE[1]
                if loc[0] < 0: loc[0] = WINDOW_SIZE[0]

            if loc[1] > WINDOW_SIZE[1]: loc[1] = 0
            if loc[0] > WINDOW_SIZE[0]: loc[0] = 0

    def draw(self, surf, color=(150, 150, 150)):
        [pygame.draw.circle(surf, pygame.Color(color), loc, 3) for loc in self.locs]


last_time = time()
densidade = 300


start_time = datetime.now()

fall = Fall(densidade)
snow = True
rain = False
laser = False
wind = 0.3
gravity = 0.3
color = (150, 150, 150)


while True:
    pygame.display.set_caption('SnowPygame. FPS: {}. Density: {}. Gravity: {:.2f}. Wind: {:.2f}.'.format(str(int(clock.get_fps())), densidade, gravity, wind))
    screen.fill((10, 10, 20))

    if snow:
        wind = 0.3
        gravity = 0.3
        color = (150, 150, 150)
    elif rain:
        wind = -0.3
        gravity = 2
        color = (60, 60, 150)
    elif laser:
        wind = 0
        gravity = -0.6
        color = (170, 30, 30)

    dt = time() - last_time
    dt *= 75
    last_time = time()

    fall.update(gravity, wind)
    fall.draw(screen, color)

    for event in pygame.event.get():
        if event.type == QUIT:
            print('\033[01;32m' + 'Duração: {}'.format(datetime.now() - start_time) + '\033[m')
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_y:
                densidade += 20
                fall = Fall(densidade)
            if event.key == K_t:
                densidade -= 20
                fall = Fall(densidade)
            if event.key == K_g:
                gravity -= 0.3
            if event.key == K_h:
                gravity += 0.3
            if event.key == K_b:
                wind -= 0.3
            if event.key == K_n:
                wind += 0.3
            if event.key == K_o:
                snow = True
                rain = False
                laser = False
            if event.key == K_k:
                snow = False
                rain = True
                laser = False
            if event.key == K_m:
                snow = False
                rain = False
                laser = True

    pygame.display.update()
    clock.tick(75)