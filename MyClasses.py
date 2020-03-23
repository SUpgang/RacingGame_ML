import pygame
import numpy as np

class Street:
    '''The street and its movement

        Attributes:
            number_of_lanes: integer
            image_lane: pygame image for one lane
            speed = (0, speed_y): numpy array
            height: equals height of one lane
            width: equals width_of_lane * number_of_lanes
            agents: list of agents on the street

    '''

    def __init__(self):
        pass


class TrafficAgents:
    '''An object on the street (including the player, enemies and fixed obstacles)

        Attributes:
            position = (pos_x, pos_y): numpy array
            lane: current lane, integer, 1-to-1 with position
            image: pygame image
            collision_rect: pygame rect to check for collisions
            speed = (speed_x, speed_y): numpy array, number of pixel to move every tick

    '''

    _number_of_agents = 0

    def __init__(self):

        TrafficAgents._number_of_agents += 1

class GameSession:
    '''The Session which handles one game including Street and Agents

        Attributes:
            street: Street-object
            player:
            screen:
            enemies_list: List of all enemies


        '''

    def __init__(self):
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

