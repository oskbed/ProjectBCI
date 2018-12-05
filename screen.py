import __future__

import pygame
import sys
import random
import multiprocessing as mp


# --- constants ---

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE =  (  0, 191, 255)

COLORS_STIMULI = [BLUE, WHITE, RED, GREEN]

# --- classes ---

class Rectangle():

    def __init__(self, color, rect, time, delay):
        self.color = color
        self.rect = rect
        self.time = time
        self.delay = delay
        self.show = False

    def draw(self, screen):
        if self.show:
            pygame.draw.rect(screen, self.color, self.rect)

    def update(self, current_time):
        if current_time >= self.time:
             self.time = current_time + self.delay
             self.show = not self.show

# --- main ---
class Signal(object):
    def __init__(self, hz):
        self.hz = hz

reference_signals = []

reference_signals.append(Signal(22))

def main(reference_signals):
    pygame.init()

    fenetre = pygame.display.set_mode((1200, 600), 0, 32)

    current_time = pygame.time.get_ticks()


    # time of show or hide

    def delay(hz):
        time = hz.hz
        delay = 1000/time
        return delay

    # same reference as signals but for rectangles
    rectangles = []


    # objects
    for i in range(len(reference_signals)):
        rect = Rectangle(random.choice(COLORS_STIMULI), ((200+i*380),150,100,50), current_time, delay(reference_signals[i]))
        rectangles.append(rect)
    #rect_red = Rectangle(RED, (100,150,100,50), current_time + 150, 100)
    #rect_green = Rectangle(GREEN, (0, 0, 500, 400), current_time + 300, 2000)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
                exit()

        # --- updates ---

        current_time = pygame.time.get_ticks()

        for i in range(len(reference_signals)):
            rectangles[i].update(current_time)

        # --- draws ---

        fenetre.fill(BLACK)

        for i in range(len(reference_signals)):
            rectangles[i].draw(fenetre)

        pygame.display.update()

prcs = mp.Process(target=main(reference_signals),
                       args=(reference_signals,))
