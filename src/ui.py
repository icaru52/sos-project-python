# File: ui.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from collections import UserDict
from collections.abc import Sequence
from typing import Dict
import pygame

BUTTON_CLICK = pygame.event.custom_type()

class Button(pygame.Rect):
    """A clickable button for Pygame"""

    def __init__(self,
                 rect: pygame.Rect,
                 text: str = "",
                 event_attrs: Dict = None,
                 clicked: bool = False,
                 color: pygame.Color = None,
                 hover_color: pygame.Color = None,
                 clicked_color: pygame.Color = None,
                 clicked_hover_color: pygame.Color = None,
                 text_color: pygame.Color = None) -> None:
    
        self.rect = rect
        self.text = text
        self.event_attrs = dict() if event_attrs is None else event_attrs
        self.clicked = clicked

        self.color               = pygame.Color("gray50") if color is None else color
        self.hover_color         = pygame.Color("gray60") if color is None else hover_color
        self.clicked_color       = pygame.Color("gray30") if color is None else clicked_color
        self.clicked_hover_color = pygame.Color("gray40") if color is None else clicked_hover_color
        self.text_color          = pygame.Color("white")  if color is None else text_color


    def is_hovered(self, pos: Sequence = None) -> bool:
        return False if pos is None else self.rect.collidepoint(pos)


    def draw(self, surface: pygame.Surface, hover: bool = True) -> None:
        cur_color = pygame.Color("blue")
        if hover and self.is_hovered(pygame.mouse.get_pos()):
            if self.clicked:
                cur_color = self.clicked_hover_color
            else:
                cur_color = self.hover_color
        else:
            if self.clicked:
                cur_color = self.clicked_color
            else:
                cur_color = self.color
        pygame.draw.rect(surface, cur_color, self.rect, 0)
        
        if self.rect.height >= 5:
            font = pygame.font.SysFont(None, 20)
            text = font.render(self.text, 1, (0,0,0))
            size = int(text.get_rect().fit(self.rect).height)
 
            font = pygame.font.SysFont(None, size)
            text = font.render(self.text, 1, self.text_color)

            surface.blit(text, text.get_rect(center=self.rect.center))

    def click(self, mouse_button: int = 1):
        outattr = self.event_attrs.copy()
        outattr["mouse_button"] = mouse_button
        pygame.event.post(pygame.event.Event(BUTTON_CLICK, outattr))


class UI(UserDict):
    #def __init__(self):
    #    pass
        
    #needs_refresh = False        

    def __setitem__(self, key: str, button: Button):
        UserDict.__setitem__(self, key, button)
        UserDict.__getitem__(self, key).event_attrs["key"] = key

    def draw(self, surface: pygame.Surface, hover: bool = True) -> None:
        for b in self.values(): b.draw(surface, hover)

    def click(self, pos: Sequence, mouse_button: int = 1) -> None:
        for b in self.values():
            if b.rect.collidepoint(pos):
                b.click(mouse_button)
                break

    def hover(self, pos: Sequence) -> str:
        for key, b in self.items():
            if b.rect.collidepoint(pos):
                return key


