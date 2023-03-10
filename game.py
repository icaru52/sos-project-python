# File: game.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

import os, pygame, sys
import board

class Button:
    def __init__(self, rect, text=""):
        

class Game:
    def __init__(self, windowWidth=512, windowHeight=512):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()

        res = (windowWidth, windowHeight)

        size = min(res[0], res[1])
        surface = pygame.display.set_mode(res)

    def menu(self):


    def play(self):
        self.surface.fill((0, 0, 0))
        for i in range(numTiles):
            for j in range(numTiles):
                tileX = (width  - size)/2 + gapSize + (tileSize + gapSize)*j
                tileY = (height - size)/2 + gapSize + (tileSize + gapSize)*i
                pygame.draw.rect(surface, (255, 100, 100), [tileX, tileY, 
                                                           tileSize, tileSize], 2)
    
    def start(self):
        running = True

        while running:
            for e in pygame.event.get():
                match e.type:
                    case pygame.QUIT:
                        running = False

                    case pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                            running = False

            pygame.display.update()
    



