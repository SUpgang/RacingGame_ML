import pygame
import mycolors

# Initialize pygame
pygame.init()
pygame.font.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Python Project')
myfont = pygame.font.SysFont('Comic Sans MS', 20)

# globale game variables
game_live = True

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