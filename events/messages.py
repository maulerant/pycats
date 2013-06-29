# -*- coding: utf-8 -*-

"""
Date: Пнд 06 Июн 2011 20:17:46
File: messages.py
Author: Igor V. Lashyn
Description: 
"""

import pygame


class Messages(pygame.sprite.DirtySprite):
    """docstring for Messages"""

    def __init__(self):
        super(Messages, self).__init__()
        self.msg = ""
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()

    def update(self, parent_rect):
        """docstring for update"""
        font = pygame.font.Font(None, 24)
        text = font.render(self.msg, 1, (255, 250, 250))
        self.rect = text.get_rect()
        self.rect.bottomleft = parent_rect.topright
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill((0, 0, 0), self.rect)
        self.image.blit(text, self.image.get_rect())
