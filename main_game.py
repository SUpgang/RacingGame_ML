import random
from MyClasses import *

# init pygame
pygame.init()
pygame.font.init()
my_screen = pygame.display.set_mode((800, 500))

## init pygame font
# font_size = 20
# myfont = pygame.font.SysFont('Comic Sans MS', font_size)

my_game_session = GameSession(screen=my_screen)

while my_game_session.live:

    my_game_session.gameloop()
    pygame.display.flip()

pygame.quit()
quit()
