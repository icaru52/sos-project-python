# File: ui.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from collections.abc import Sequence
#import math
import pygame

BUTTON_CLICK = pygame.event.custom_type()

class Button(pygame.Rect):
    """A clickable button for Pygame"""

    def __init__(self,
                 rect: pygame.Rect,
                 event_attr: str = "",
                 text: str = "",
                 clicked: bool = False,
                 color: pygame.Color = None,
                 hover_color: pygame.Color = None,
                 text_color: pygame.Color = None) -> None:
    
        self.rect = rect
        #self.rect = pygame.Rect(0, 0, 1, 1) if rect is None else rect
        self.color = pygame.Color("darkgray") if color is None else color
        self.hover_color = pygame.Color("gray") if color is None else hover_color
        self.text_color = pygame.Color("white") if color is None else text_color

        self.text = text
        self.event_attr = event_attr
        self.clicked = clicked

    def is_hovered(self, pos: Sequence) -> bool:
        return self.collidepoint(pos)

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

        pygame.draw.rect(surface, current_color, self.rect, 2)
        
        if self.rect.height >= 10:
            font = pygame.font.SysFont(None, int(self.rect.height))
            text = font.render(self.text, 1, self.text_color)
            surface.blit(text, text.get_rect(center=self.rect.center))
    
    def click(self):
        pygame.event.post(
                pygame.event.Event(BUTTON_CLICK, {"button" : self.event_attr}))


class UI:
    def __init__(self) -> None:
        self.buttons = list()

    def add(self, button: Button) -> bool:
        if button.collidelist(self.buttons) == -1:
            self.buttons.append(button)
            return True
        else:
            return False

    def draw(self, surface: pygame.Surface) -> None:
        for b in self.buttons:
           b.draw(surface) 

    def click(self, pos: Sequence) -> None:
        for b in self.buttons:
            if b.rect.collidepoint(pos):
                b.click()
                return

        #index = pygame.Rect(pos, (0, 0)).collidelist(self.buttons)
        #if index != -1:
        #    self.buttons[index].click()


