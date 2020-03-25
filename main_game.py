from MyClasses import *

# global settings
number_of_sessions = 2

# init pygame
pygame.init()
pygame.font.init()
my_screen = pygame.display.set_mode((1000, 500))
my_surface = pygame.Surface((1000,500))

# Camera rectangles for sections of  the canvas
game1 = pygame.Rect(0,0,500,500)
game2 = pygame.Rect(500,0,500,500)

image = pygame.image.load('car_sprite.png')

# subsurfaces of canvas
# Note that subx needs refreshing when px_camera changes.
sub1 = my_surface.subsurface(game1)
sub2 = my_surface.subsurface(game2)

while True:
    sub1.blit(image, (0,0))
    my_screen.blit(sub1, (0,0))
    my_screen.blit(sub1, (500, 0))
    # game2.fill(mycolors.blue)
    pygame.display.flip()

quit()


## init pygame font
# font_size = 20
# myfont = pygame.font.SysFont('Comic Sans MS', font_size)

session_list = []

session_list.append(GameSession(screen=my_screen))

for i in range(number_of_sessions):
    session_list.append(GameSession())

while my_game_session.live:

    my_game_session.gameloop()
    pygame.display.flip()

pygame.quit()
quit()
