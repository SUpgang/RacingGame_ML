import pygame
import mycolors
import time

# Initialize pygame
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 20

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Python Project')
myfont = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)

# globale game variables
game_live = True

# Test Area
myRect = pygame.Rect(0,100,50,50)
stepw = 10

while game_live:
    time.sleep(0.01)
    screen.fill(mycolors.white)
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_live = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                myRect.y -= stepw
            if event.key == pygame.K_DOWN:
                myRect.y += stepw
            if event.key == pygame.K_LEFT:
                myRect.x -= stepw
            if event.key == pygame.K_RIGHT:
                myRect.x += stepw


    # Draw things
    pygame.draw.rect(screen, mycolors.green, myRect)
    pygame.display.flip()




# Quit game after loop
pygame.quit()