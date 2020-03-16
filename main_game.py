import pygame as pg
import mycolors

# Initialize pygame
pg.init()
pg.font.init()

# Create the screen
screen = pg.display.set_mode((800, 600))
pg.display.set_caption('Python Project')
myfont = pg.font.SysFont('Comic Sans MS', 20)

# globale game variables
game_live = True

myRect = pg.Rect(100, 100, 50, 50)

while game_live:
    pg.draw.rect(screen, mycolors.green, myRect)
