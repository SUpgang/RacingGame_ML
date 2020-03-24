import pygame
import numpy as np
import mycolors

class TrafficAgents:
    """An object on the street (including the player, enemies and fixed obstacles)

        Attributes:
            agent_type: 'enemy' for enemy car, 'player' for player
            lane: current lane, integer, 1-to-1 with position
            position = (pos_x, pos_y): numpy array
            speed = (speed_x, speed_y): numpy array, number of pixel to move every tick
            image: pygame image
            collision_rect: pygame rect to check for collisions

        Methods:
            update_position(self)
            check_collision(self, other_rect)
            get_pos_x(self): returns the pos_x according to self.lane

    """
    _number_of_agents = 0

    def __init__(self, game_session, starting_lane=1, agent_type='enemy'):
        self._game_session = game_session
        self.lane = starting_lane
        self.agent_type = agent_type
        if agent_type != '':
            self.image_width = 60
            self.image_height = 100
            self.pos_x = self._game_session.lane_width*(self.lane-1) + (self._game_session.lane_width-self.image_width)/2
            if agent_type == 'player':
                self.image = pygame.image.load('car_sprite.png')
                self.pos_y = self._game_session.screen.get_height()-self.image_height
                self.speed_x = 1
                self.speed_y = 1
            else:
                self.image = pygame.image.load('car_sprite_enemy.png')
                self.pos_y = -self.image_height
                self.speed_x = 0
                self.speed_y = 2
            self.position = np.array([self.pos_x,self.pos_y])
            self.speed = np.array([self.speed_x,self.speed_y])
            self.collision_rect = pygame.Rect((self.pos_x, self.pos_y), (self.image_width, self.image_height))

        TrafficAgents._number_of_agents += 1


    def get_pos_x(self):
        self.pos_x = self._game_session.lane_width * (self.lane - 1) + (self._game_session.lane_width - self.image_width) / 2

    def update_position(self):
        self.pos_y = self.pos_y + self.speed_y
        self.collision_rect.move_ip(0, self.speed_y)

    def check_collision(self, other_rect):
        return self.collision_rect.colliderect(other_rect.collision_rect)
        

class GameSession:
    """ Underlying object which manages all parts of a GameSession

        Attributes:
            req_screen_height: requiered screen height
            req_screen_width: requiered screen width
            FPS: 60
            game_clock: clock for the game to count the loops

            lane_image = 'street_sprite.png'
            lane_width = 100: given by pixels of picture
            lane_height = 500: given by pixels of picture

            number_of_lanes: integer

            sprite_position = (pos_x, pos_y): numpy array, starting value to draw lanes
            speed = (0, speed_y): numpy array

            enemies_list: list of enemies on the street

            live = True: status of the game, running or not

        Methods:
            tick()
            draw_street(self)
    """

    def __init__(self, number_of_lanes=8, lane_sprite='street_sprite.png', fps=60, screen=[]):
        """ """

        # init game_clock
        self.game_clock = pygame.time.Clock()
        self.FPS = fps
        self.screen = screen

        # load street sprite
        self.lane_image = pygame.image.load(lane_sprite)
        self.lane_height = self.lane_image.get_height()
        self.lane_width = self.lane_image.get_width()

        # init further attributes
        self.number_of_lanes = number_of_lanes
        self.enemies_list = []
        self.t = 0

        # init screen
        self.req_screen_height = self.lane_height
        self.req_screen_width = number_of_lanes * self.lane_width
        if not screen == []:
            self.screen = pygame.display.set_mode((self.req_screen_width, self.req_screen_height))

        self.live = True

    def tick(self):
        self.game_clock.tick(self.FPS)
        self.t += 1
        #print(self.t)

    def draw_street(self, speed=1):
        """Draws the street to screen according to the current speed"""

        if not self.screen == []:
            self.screen.fill(mycolors.white)
            self.screen.blit(self.lane_image, (0,100))

            # Fill up the streets:
            for i in range(self.number_of_lanes):
                cycle = int(self.lane_height/speed)
                shift_px_y = speed * self.t % cycle
                self.screen.blit(self.lane_image, (self.lane_width * i, shift_px_y))
                self.screen.blit(self.lane_image, (self.lane_width * i, -self.lane_height + shift_px_y))

    def handle_events(self):
        """For events like quit or userinputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.live = False

    def gameloop(self):
        """All functions needed for one loop cycle"""
        self.tick()
        self.handle_events()
        self.draw_street()



class Enemy:
    """Enemies which occur on the lanes"""

    def __init__(self, starting_lane = 1, image='car_sprite_enemy.png', street_width = 100, speed_delta_px_per_tick = 1):

        self.lane = starting_lane
        self._image_filename = image
        self._street_width = street_width
        self._delta_px_per_tick = speed_delta_px_per_tick

        if image != '':
            self.image = pygame.image.load(image)
            self.image_width = 60
            self.image_height = 100
            self.pos_y_puffer_px = self.image_height

        self.pos_x = 20 + (self.lane-1) * self._street_width
        self.pos_y = -self.pos_y_puffer_px
        self.collision_rect = pygame.Rect((self.pos_x, self.pos_y), (60, 100))

    def update_position(self):
        self.pos_y = self.pos_y + self._delta_px_per_tick
        self.collision_rect.move_ip(0, self._delta_px_per_tick)

