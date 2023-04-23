# File: ui.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from collections.abc import Sequence
#import math
import pygame

class Button:
    """A clickable button for Pygame"""

    def __init__(self,
                 rect: pygame.Rect = None,
                 color: pygame.Color = None,
                 hover_color: pygame.Color = None,
                 text_color: pygame.Color = None,
                 text: str = "",
                 click_func) -> None:
        
        self.rect = pygame.Rect(0, 0, 1, 1) if rect is None else rect
        self.color = pygame.Color("darkgray") if color is None else color
        self.hover_color = pygame.Color("gray") if color is None else hover_color
        self.text_color = pygame.Color("white") if color is None else text_color

        self.text = text
        self.clicked = clicked

        self.click = click_func

    def is_hovered(self, pos: Sequence) -> bool:
        return self.rect.collidepoint(pos)

    def draw(self, surface: pygame.Surface) -> None:

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.clicked:
                current_color = self.clicked_hover_color
            else:
                current_color = self.hover_color
        else:
            if self.clicked:
                current_color = self.clicked_color
            else:
                current_color = self.color

        pygame.draw.rect(surface, self.current_color, self.rect, 2)

        if self.rect.get_height() >= 10:
            font = pygame.font.SysFont(None, int(self.rect.get_height()))
            text = font.render(self.text, 1, self.text_color)
            surface.blit(text, text.get_rect(center=self.rect.center))


class UI:
    def __init__(self) -> None:
        self.buttons = list()

    def add(self, button: Button) -> None:
        for b in self.buttons:
            if b.rect.colliderect(button.rect):
                return

        self.buttons.append(button)

    def draw(self, surface: pygame.Surface) -> None:
        for b in self.buttons:
           b.draw(surface) 

    def click(self, pos: Sequence) -> None:
        for b in self.buttons:
            if b.rect.collidepoint(pos):
                b.click()
                return


