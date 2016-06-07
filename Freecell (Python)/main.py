#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, random
from pygame.locals import *
from classes import *

#===============================================================
# Constants
#===============================================================

SCREENWIDTH, SCREENHEIGHT = 890, 600   # Intial Window size
BGCOLOR = (80,180,80)                  # Window background colour (green)
FPS = 24                               # frames per second

WINDOW_CAPTION = "Freecell By Ricky Bertram"
WINDOW_ICON_PATH = "heart.jpg"

#===============================================================
# Window Setup
#===============================================================

# Start pygame
pygame.init()

# Pygame Screen
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), RESIZABLE)

# Application Title
pygame.display.set_caption(WINDOW_CAPTION)

# Application Icon
pygame.display.set_icon(pygame.image.load(WINDOW_ICON_PATH))

clock = pygame.time.Clock()

deck = []
cards = []
suitPiles = []
freecells = []
selectedCards = None
screenwidth = SCREENWIDTH
screenheight = SCREENHEIGHT

image_heart = pygame.image.load("heart.jpg")
image_club = pygame.image.load("club.jpg")
image_diamond = pygame.image.load("diamond.jpg")
image_spade = pygame.image.load("spade.jpg")
CARD_IMAGES = { 'heart': image_heart, 'club': image_club, 'diamond': image_diamond, 'spade': image_spade }


def main():

    global screen
    global deck
    global cards
    global screenwidth
    global screenheight
    global CARD_IMAGES
    global selectedCards
    global freecells
    global suitPiles
    
    gameStarted = False
    dragMode = False
    clickedCardX = 0
    clickedCardY = 0
    maxDraggableCards = 0
    
    while True:
        
        screen.fill(BGCOLOR)
        
        for event in pygame.event.get():

            # Exit Game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Window Resize
            elif event.type == VIDEORESIZE:
                screenwidth, screenheight = event.dict['size']
                screen = pygame.display.set_mode(event.dict['size'], RESIZABLE)
                pygame.display.flip()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # See if we have a card
                selectedCards = findClickedCards(event.pos)
                if not selectedCards == None:
                    clickedCardX = selectedCards[0].rect.x # location to revert to if not dropped somewhere sensible
                    clickedCardY = selectedCards[0].rect.y
                dragMode = True
                
            elif event.type == pygame.MOUSEMOTION:
                # Mouse moved
                if dragMode and not selectedCards == None:
                    # Move the card(s)
                    i = 0
                    for card in selectedCards:
                        card.rect.x = event.pos[0]
                        card.rect.y = event.pos[1] + 30 * i
                        i += 1
                
            elif event.type == pygame.MOUSEBUTTONUP:
                # mouse released
                if not selectedCards == None:
                    if dropCheck():
                        # card has been moved
                        pass
                    else:
                        # Revert to original positions
                        i = 0
                        for card in selectedCards:
                            card.rect.x = clickedCardX
                            card.rect.y = clickedCardY + 30 * i
                            i += 1
                dragMode = False
                selectedCards = None

        # Check if this is a new game
        if gameStarted == False:
            # Yes - create deck
            gameStarted = True
            maxDraggableCards = 5
            deck = newDeck()

        # Output deck
        drawBoard()
        drawCards()

        pygame.display.update()
        clock.tick(FPS)


def drawBoard():

    global freecells
    global suitPiles
    
    # Finished Suits
    if len(suitPiles) == 0:
        suitPiles.append(CardHolder(screen, screenwidth - 100 - 10, 10, 15))
        suitPiles.append(CardHolder(screen, screenwidth - 200 - 20, 10, 14))
        suitPiles.append(CardHolder(screen, screenwidth - 300 - 30, 10, 13))
        suitPiles.append(CardHolder(screen, screenwidth - 400 - 40, 10, 12))

    for pile in suitPiles:
        pile.draw()

    # Freecells
    if len(freecells) == 0:
        freecells.append(CardHolder(screen,  10, 10, 8))
        freecells.append(CardHolder(screen, 120, 10, 9))
        freecells.append(CardHolder(screen, 230, 10, 10))
        freecells.append(CardHolder(screen, 340, 10, 11))

    for freecell in freecells:
        freecell.draw()

        
# called onmousedown
def findClickedCards(mousePosition):
    x = 0
    xMin = 10
    xMax = 110
    for column in deck:

        if mousePosition[0] > xMin and mousePosition[0] < xMax:
            # Applicable to this column(?)
            y = 0
            
            for card in column:

                # Check not bottom card and y position
                if y < len(column) - 1 and (mousePosition[1] > card.rect.top and mousePosition[1] < card.rect.top + 30):
                    
                    z = y
                    cards = [card]
                    
                    while z < len(column) - 1:
                        tempCard = deck[x][z]
                        childCard = deck[x][z+1]
                        
                        if tempCard.suit == 'S' or tempCard.suit == 'C':
                            # 1st card is black
                            if childCard.suit == 'S' or childCard.suit == 'C' or int(childCard.number) != (int(tempCard.number) - 1):
                                # 2nd card is not next in sequence
                                return None
                        else:
                            # 1st card is red
                            if childCard.suit == 'D' or childCard.suit == 'H' or int(childCard.number) != (int(tempCard.number) - 1):
                                # 2nd card is not next in sequence
                                return None
                        z += 1
                        cards.append(childCard)

                    # If we are here then all is ok!
                    return cards
                    
                elif y == len(column) - 1 and (mousePosition[1] > card.rect.top and mousePosition[1] < card.rect.bottom):
                    # Bottom Card
                    return [card]

                else:
                    pass
                
                y += 1
            
        else:
            # Ignore Column
            pass

        # Adjust column seek
        xMin = xMax + 10
        xMax = xMin + 100
        x += 1
    
    # Check freecells
    for freecell in freecells:
        if len(freecell.pile) == 1:
            if mousePosition[0] > freecell.rect.x and mousePosition[0] < freecell.rect.x + 100 and mousePosition[1] > freecell.rect.y and mousePosition[1] < freecell.rect.y + 140:
                return [freecell.pile[0]]
        

def dropCheck():

    global freecells
    global selectedCards
    global deck
    
    if len(selectedCards) == 1:
        # dragging one card - check if we are trying to put in a 'freecell'
        for freecell in freecells:
            if selectedCards[0].rect.colliderect(freecell.rect):
                if len(freecell.pile) == 0:
                    # empty - allow to add
                    # remove from column array
                    if selectedCards[0].columnKey < 8:
                        # Was in standard row
                        deck[selectedCards[0].columnKey].pop()
                    else:
                        # Was in a freecell
                        freecells[selectedCards[0].columnKey - 8].pile = []

                    # Move position
                    selectedCards[0].rect.x = freecell.rect.x
                    selectedCards[0].rect.y = freecell.rect.y
                    selectedCards[0].columnKey = freecell.columnKey

                    # Add to freecell
                    freecell.add(selectedCards[0])
                    
                    return True
                else:
                    # return False
                    pass

        # dragging one card - check if we are trying to put in a 'suit pile'
        for suitPile in suitPiles:
            if selectedCards[0].rect.colliderect(suitPile.rect):
                
                # check if the card is correct
                if len(suitPile.pile) > 0:
                    # There are already cards in this pile
                    canDrop = (selectedCards[0].suit == suitPile.pile[-1].suit and int(selectedCards[0].number) == int(suitPile.pile[-1].number) + 1)
                else:
                    # No cards - check for Ace
                    canDrop = (selectedCards[0].caption == "A")

                if canDrop:
                    
                    # remove from column array
                    if selectedCards[0].columnKey < 8:
                        # Was in standard row
                        deck[selectedCards[0].columnKey].pop()
                    else:
                        # Was in a freecell
                        freecells[selectedCards[0].columnKey - 8].pile = []

                    # Move position
                    selectedCards[0].rect.x = suitPile.rect.x
                    selectedCards[0].rect.y = suitPile.rect.y
                    selectedCards[0].columnKey = suitPile.columnKey
                    
                    # Add to freecell
                    suitPile.add(selectedCards[0])
                    
                    return True
                else:
                    # return False
                    pass
    
    # Check for drop onto main deck
    return dropCheck_MainDeck()
    

# Check for actions on dropping a card onto one of the 8 main deck columns
def dropCheck_MainDeck():
    
    global deck
    global selectedCards

    # Stop here if we aren't allow to move this many cards!
    if len(selectedCards) > numCardsPermittedToMove():
        return False
    
    c = 0
    for column in deck:
        if len(column) > 0:
            lastCard = column[len(column) - 1]
            if selectedCards[0].rect.colliderect(lastCard.rect):
                # dropping onto a column
                if lastCard.suit == 'S' or lastCard.suit == 'C':
                    # Dropping onto a black card
                    if int(lastCard.number) == int(selectedCards[0].number) + 1 and (selectedCards[0].suit == 'H' or selectedCards[0].suit == 'D'):
                        # Yes! We've found a suitable match
                        return appendSelectedToColumn(c)
                else:
                    # Dropping onto a red card
                    if int(lastCard.number) == int(selectedCards[0].number) + 1 and (selectedCards[0].suit == 'S' or selectedCards[0].suit == 'C'):
                        # Yes! We've found a suitable match
                        return appendSelectedToColumn(c)
                    
        else:
            # Column length = 0
            # This collision detection could be tidier!
            # just created an area for this column (+ 500 is made up!)
            if selectedCards[0].rect.x > c * 110 + 10 and selectedCards[0].rect.x < c * 110 + 10 + 100 and selectedCards[0].rect.y > 180 and selectedCards[0].rect.y < 180 + 500:

                # Add to new column
                return appendSelectedToColumn(c)
                
        c += 1
        
    return False


# Calculate the number of cards we can move based on the number of freecells
def numCardsPermittedToMove():

    global freecells

    count = 1

    for freecell in freecells:
        if len(freecell.pile) == 0:
            count += 1
            
    return count


# Append the selected cards to the deck column
def appendSelectedToColumn(columnIndex):
    
    global deck
    global selectedCards
    global freecells
    
    for i in range(0, len(selectedCards)):

        if selectedCards[i].columnKey < 8:
            # Was in standard row
            deck[selectedCards[i].columnKey].pop()
        else:
            # Was in a freecell
            freecells[selectedCards[i].columnKey - 8].pile = []
        
        selectedCards[i].columnKey = columnIndex
        
        if len(deck[columnIndex]) > 0:
            # Set position relative to current last card
            lastCard = deck[columnIndex][len(deck[columnIndex]) - 1]
            deck[columnIndex].append(selectedCards[i])
            selectedCards[i].rect.x = lastCard.rect.x
            selectedCards[i].rect.y = lastCard.rect.y + 30
            
        else:
            # Add to top of column
            deck[columnIndex].append(selectedCards[i])
            selectedCards[i].rect.x = columnIndex * 110 + 10
            selectedCards[i].rect.y = 180 # constant height from top
            
    return True
            


# Draw (print) the cards on the screen
def drawCards():

    global selectedCards
    global freecells
    global suitPiles
    
    for column in deck:
        for card in column:
            if selectedCards == None:
                # print "not selected"
                card.draw()
            else:
                for selectedCard in selectedCards:
                    if card.cardID == selectedCard.cardID:
                        pass
                    else:
                        card.draw()

    for freecell in freecells:
        for card in freecell.pile:
            card.draw()

    for suitPile in suitPiles:
        for card in suitPile.pile:
            card.draw()
    
    if not selectedCards == None:
        # draw selected cards after (correct z-index)
        for selectedCard in selectedCards:
            selectedCard.draw()
    
    
def newDeck():

    deck = []

    for suit in ('H','S','D','C'):
        for value in range(1, 14):
            deck.append(suit + str(value))
    
    random.shuffle(deck)

    columns = [[],[],[],[],[],[],[],[]]

    # split into 8 columns
    for i in range(0, 52):
        xpos = 10 + 110 * (i % 8)
        ypos = 180 + abs(i / 8) * 30
       # print "x=" + str(xpos)
       # print "y=" + str(ypos)
        columns[i % 8].append(Card(deck[i-1], screen, xpos, ypos, (i % 8), CARD_IMAGES))
        
    return columns


if __name__ == '__main__':
    main()
