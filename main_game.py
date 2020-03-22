import pygame
import mycolors
import myclasses as mc
import numpy as np
import time

# Initialize pygame
pygame.init()
pygame.font.init()

myclock = pygame.time.Clock()
FPS = 60

# Sound
#crash = pygame.mixer.music.load('collision.MP3')

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

player_car = mc.MyCar(image='car_sprite.png')
player_car.pos_y = SCREEN_HEIGHT-player_car.image_height

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

    #Draw player_car
    player_car.update_x()
    screen.blit(player_car.image, (player_car.pos_x,player_car.pos_y))

    #Let enemy cars drive
    if collision == False:
        for enemy in list_of_enemies:
            enemy.update_position()
    #list_of_enemies = [e.update_position() for e in list_of_enemies]

    #Update list_of_enemies if starting position is free
    if np.random.binomial(1, 0.01) == True:
        random_lane=np.random.randint(0, number_of_lanes+1)
        y_help = np.array([enemy.pos_y for enemy in list_of_enemies])
        lane_help = np.array([enemy.lane for enemy in list_of_enemies])
        if not min(list(y_help[np.where(lane_help == random_lane)]), default=car_height+1)<=car_height:
            enemy = mc.Enemy(random_lane, 'car_enemy.png')
            list_of_enemies.append(enemy)
       
    #Delete enemies from list_of_enemies if they leave the screen
    for i,enemy in enumerate(list_of_enemies):
        if (enemy.pos_y>SCREEN_HEIGHT):
            del list_of_enemies[i]
        screen.blit(enemy.image, (enemy.pos_x, enemy.pos_y))

    #Check for collision
    y_help = np.array([enemy.pos_y for enemy in list_of_enemies])
    lane_help = np.array([enemy.lane for enemy in list_of_enemies])
    if player_car.pos_y-max(list(y_help[np.where(lane_help == player_car.lane)]), default=car_height+1)<=car_height:
        collision = True
        #pygame.mixer.music.play()


    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_live = False
        if (event.type == pygame.KEYDOWN) and (collision == False):
            if event.key == pygame.K_LEFT:
                player_car.lane = max(1, player_car.lane - 1)
            if event.key == pygame.K_RIGHT:
                player_car.lane = min(number_of_lanes, player_car.lane + 1)

    # Show drawings on screen
    pygame.display.flip()
    if collision == False:
        tick += 1


# Quit game after loop
pygame.quit()
quit()
