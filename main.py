#!/usr/bin/env python3

# File: main.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

import os, pygame, sys
import board

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    width = 512
    height = 512

    size = min(width, height)
    numTiles = 8
    board = board.Board(numTiles, numTiles)
    gapSize = size*0.01
    tileSize = (size - gapSize) / numTiles - gapSize

    screen = pygame.display.set_mode((width, height))

    for i in range(numTiles):
        for j in range(numTiles):
            tileX = (width - size)/2 + gapSize + (tileSize + gapSize)*j
            tileY = (height - size)/2 + gapSize + (tileSize + gapSize)*i
            pygame.draw.rect(screen, (255, 100, 100), [tileX, tileY, 
                                                       tileSize, tileSize], 2)
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
    


