import pygame
import mycolors
import random
import MyClasses

# Initialize pygame
pygame.init()
pygame.font.init()

myclock = pygame.time.Clock()
FPS = 60

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
car_current_lane = car_starting_lane
tick = 0
delta_px_per_tick = 2
cycle = int(lane_height/delta_px_per_tick)
p = 0
enemy_list = []

while game_live:
    myclock.tick(FPS)

    # Delete previous content
    screen.fill(mycolors.white)

    # Fill up the streets:
    for i in range(number_of_lanes):
        shift_px_y = delta_px_per_tick*tick%cycle
        screen.blit(lane_image, (lane_width*i, shift_px_y))
        screen.blit(lane_image, (lane_width*i, -lane_height + shift_px_y))

    screen.blit(car_image, (lane_width*(car_current_lane-1) + 20, 400))
    # 20 px

    # Create enemies
    if random.random() < p:
        starting_lane = random.randint(1, number_of_lanes)
        enemy_list.append(MyClasses.Enemy(starting_lane=starting_lane))
        p = 0
    else:
        p += round(1 / ((len(enemy_list)+1)*FPS*100),6)

    for i, enemy in enumerate(enemy_list):
        enemy.update_position()
        screen.blit(enemy.image, (enemy.pos_x, enemy.pos_y))
        if enemy.pos_y > 500:
            enemy_list.pop(i)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_live = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car_current_lane = max(1, car_current_lane - 1)
            if event.key == pygame.K_RIGHT:
                car_current_lane = min(number_of_lanes, car_current_lane + 1)

    # Show drawings on screen
    pygame.display.flip()
    tick += 1

# Quit game after loop
pygame.quit()
quit()
