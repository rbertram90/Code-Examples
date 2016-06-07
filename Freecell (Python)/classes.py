#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys

class Card:

    cardID = 0
    rect = None
    screen = None
    suit = ""      # S(pade), C(lub), D(iamond), H(eart)
    number = ""    # 1(A),2,3,...,10,11(J),12(Q),13(K)
    caption = ""   # A,2,3,4,5,6,7,8,9,10,J,Q,K
    image = None
    columnKey = -1
    
    def __init__(self, ID, Screen, PosX, PosY, Column, Images):
        # intialise card
        self.rect = pygame.Rect(PosX, PosY, 100, 140)
        self.cardID = ID
        self.suit = ID[0]
        self.columnKey = Column
        
        if self.suit == 'D':
            self.image = Images['diamond']
        elif self.suit == 'H':
            self.image = Images['heart']
        elif self.suit == 'C':
            self.image = Images['club']
        else:
            self.image = Images['spade']
            
        self.number = ID[1:]
        
        if self.number == "1":
            self.caption = "A"
        elif self.number == "11":
            self.caption = "J"
        elif self.number == "12":
            self.caption = "Q"
        elif self.number == "13":
            self.caption = "K"
        else:
            self.caption = self.number
        
        self.screen = Screen
        

    def draw(self):
        # Draw the card to the screen
        pygame.draw.rect(self.screen, (255,255,255), (self.rect.x, self.rect.y, 100, 140), 0)
        pygame.draw.rect(self.screen, (0,0,0), (self.rect.x, self.rect.y, 100, 140), 1)
        
        font = pygame.font.Font(None, 20)
        text = font.render(self.caption, 1, (0,0,0))
        self.screen.blit(text, (self.rect.x + 25, self.rect.y + 5))
        
        self.screen.blit(self.image, (self.rect.x + 3, self.rect.y + 3))


class CardHolder:

    # pile = []
    # rect = None
    #  screen = None

    def __init__(self, Screen, PosX, PosY, Column):
        self.screen = Screen
        self.rect = pygame.Rect(PosX, PosY, 100, 140)
        self.pile = []
        self.columnKey = Column

    def draw(self):
        pygame.draw.rect(self.screen, (0,0,0), (self.rect.x, self.rect.y, 100, 140), 1)

    def add(self, card):
        self.pile.append(card)
    
