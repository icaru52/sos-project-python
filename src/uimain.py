#!/usr/bin/env python3

# File: uimain.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from collections.abc import Sequence
import os
import pygame

import ui

if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    surface = pygame.display.set_mode((512, 512))

    keypad = ui.UI()

    keypad.add(ui.Button(pygame.Rect(100, 100, 100, 100),
    #keypad.add(ui.Button((100, 100, 100, 100),
                         "testbutton",
                         "Button",
                         False,
                         pygame.Color("darkgray"),
                         pygame.Color("gray"),
                         pygame.Color("white")))

    #x = lambda: print("Hello world!")
    #x()

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

                case pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    keypad.click(pos)
                case ui.BUTTON_CLICK:
                    print("hello")

        keypad.draw(surface)

        pygame.display.update()

