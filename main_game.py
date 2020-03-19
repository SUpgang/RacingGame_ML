import pygame
import mycolors
import myclasses  as mc
import numpy as np
import time

# Initialize pygame
pygame.init()
pygame.font.init()

myclock = pygame.time.Clock()
FPS = 60

# Sound
crash = pygame.mixer.music.load('collision.MP3')

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
FONT_SIZE = 20

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Racing Game')
myfont = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)

# global game variables
game_live = True

# Import images for lanes and cars
lane_image = pygame.image.load('street_sprite.png')
lane_height = 500
lane_width = 100

car_image = pygame.image.load('car_sprite.png')
car_height = 100
car_width = 60

# Game settings
number_of_lanes = 8
car_starting_lane = 1
tick = 0
delta_px_per_tick = 2
cycle = int(lane_height/delta_px_per_tick)
collision = False

me = mc.MyCar(image='car_sprite.png')
me.pos_y = SCREEN_HEIGHT-me.image_height

list_of_enemies = []

while game_live:
    myclock.tick(FPS)
    # time.sleep(0.01)

    # Delete previous content
    screen.fill(mycolors.white)

    # Fill up the streets:
    for i in range(number_of_lanes):
        screen.blit(lane_image, (lane_width*i, delta_px_per_tick*tick%cycle))
        screen.blit(lane_image, (lane_width*i, -lane_height+delta_px_per_tick*tick%cycle))


    me.update_x()
    screen.blit(me.image, (me.pos_x,me.pos_y))

    if collision == False:
        for e in list_of_enemies:
            e.update_position()
    #list_of_enemies = [e.update_position() for e in list_of_enemies]


    if (np.random.binomial(1, 0.01) == True):
        random_lane=np.random.randint(0, number_of_lanes+1)
        y_help = np.array([e.pos_y for e in list_of_enemies])
        lane_help = np.array([e.lane for e in list_of_enemies])
        if not min(list(y_help[np.where(lane_help == random_lane)]), default=car_height+1)<=car_height:
            enemy = mc.Enemy(random_lane, 'car_enemy.png')
            list_of_enemies.append(enemy)
       
    for i,e in enumerate(list_of_enemies):
        if (e.pos_y>SCREEN_HEIGHT):
            del list_of_enemies[i]
        screen.blit(e.image, (e.pos_x, e.pos_y))

    y_help = np.array([e.pos_y for e in list_of_enemies])
    lane_help = np.array([e.lane for e in list_of_enemies])
    if me.pos_y-max(list(y_help[np.where(lane_help == me.lane)]), default=car_height+1)<=car_height:
        collision = True
        pygame.mixer.music.play()


    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_live = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                me.lane = max(1, me.lane - 1)
            if event.key == pygame.K_RIGHT:
                me.lane = min(number_of_lanes, me.lane + 1)

    # Show drawings on screen
    pygame.display.flip()
    if collision == False:
        tick += 1


# Quit game after loop
pygame.quit()
quit()
