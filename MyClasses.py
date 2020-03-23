import pygame
import numpy as np

class Street:
    '''The street and its movement

        Attributes:
            number_of_lanes: integer
            image_lane: pygame image for one lane
            sprite_position = (pos_x, pos_y): numpy array, starting value to draw lanes
            speed = (0, speed_y): numpy array
            street_height: equals height of one lane
            street_width: equals width_of_lane * number_of_lanes
            enemies_list: list of enemies on the street

        Methods:
            update_sprite_position(self)

    '''

    def __init__(self):
        pass


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
                self.pos_y = self._game_session.screen.get_height-self.image_height
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
        

class GameSession:
    '''The Session which handles one game including Street and Agents

        Attributes:
            screen: Screen object from pygame
            street: Street-object
            player:

        Methods:

    '''

    # number_of_lanes = 8
    # car_starting_lane = 1
    # car_current_lane = car_starting_lane
    # tick = 0
    # delta_px_per_tick = 2
    # cycle = int(lane_height / delta_px_per_tick)
    # p = 0
    # enemy_list = []

    def __init__(self, height=800, width=500, starting_lane=1, h):
        pass

class Enemy:
    '''Enemies which occur on the lanes'''

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

