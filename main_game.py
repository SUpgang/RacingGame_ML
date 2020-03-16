import pygame
import mycolors

# Initialize pygame
pygame.init()
pygame.font.init()

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600
FONT_SIZE = 20

# Create the screen
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
pygame.display.set_caption('Python Project')
myfont = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)

# globale game variables
game_live = True

# Test Area
myRect = pygame.Rect(100, 100, 50, 50)

while game_live:

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_live = False

    # Draw things
    pygame.draw.rect(screen, mycolors.green, myRect)
    pygame.display.flip()

# Quit game after loop
pygame.quit()