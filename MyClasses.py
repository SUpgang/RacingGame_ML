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
            image_width: width of image in pixels
            image_height: width of image in pixels
            collision_rect: pygame rect to check for collisions
            _lane_width: lane width in pixels
            _screen_height: screen height in pixels

        Methods:
            update_position(self)
            check_collision(self, other_rect)
            get_pos_x(self): returns the pos_x according to self.lane

    """
    _number_of_agents = 0

    def __init__(self, screen_height, lane_width, starting_lane=1, agent_type='enemy'):
        self.lane = starting_lane
        self._lane_width = lane_width
        self._screen_height = screen_height
        self.agent_type = agent_type
        if agent_type == 'player':
            self.image = pygame.image.load('car_sprite.png')
            self.image_height = self.image.get_height()
            pos_y = screen_height-self.image_height
            speed_x = 0
            speed_y = 0
        else:
            self.image = pygame.image.load('car_sprite_enemy.png')
            self.image_height = self.image.get_height()
            pos_y = -self.image_height
            speed_x = 0
            speed_y = 2
        self.image_width = self.image.get_width()
        self.position = np.array([self.get_pos_x(),pos_y])
        self.speed = np.array([speed_x,speed_y])
        self.collision_rect = pygame.Rect((self.position[0], self.position[1]), (self.image_width, self.image_height))

        TrafficAgents._number_of_agents += 1

    def get_pos_x(self):
        return self._lane_width * (self.lane - 1) + (self._lane_width - self.image_width) / 2

    def update_position(self, manual_player_speed):
        if self.agent_type == 'player':
            self.speed = manual_player_speed
        self.position += self.speed
        self.collision_rect.move_ip(self.speed[0], self.speed[1])

    def check_collision(self, other_rect):
        return self.collision_rect.colliderect(other_rect.collision_rect)

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))
        

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

            agent_list: agent[0] is always the player

            live = True: status of the game, running or not

        Methods:
            tick()
            draw_street(self)
    """

    def __init__(self, player_type = 'manual', number_of_lanes=8, lane_sprite='street_sprite.png', fps=60, screen=[]):
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
        self.agent_list = []
        self.man_player_speed = np.array([0,0])
        self.t = 0

        # init screen
        self.req_screen_height = self.lane_height
        self.req_screen_width = number_of_lanes * self.lane_width
        if not screen == []:
            self.screen = pygame.display.set_mode((self.req_screen_width, self.req_screen_height))

        self.agent_list.append(TrafficAgents(agent_type='player', screen_height=self.req_screen_height, lane_width=self.lane_width))
        self.live = True

    def tick(self):
        self.game_clock.tick(self.FPS)
        self.t += 1

    def handle_events(self):
        """For events like quit or userinputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.live = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.man_player_speed[0] = -self.lane_width
                if event.key == pygame.K_RIGHT:
                    self.man_player_speed[0] = self.lane_width

    def update_positions(self):
        for agent in self.agent_list:
            agent.update_position(self.man_player_speed)
            self.man_player_speed = np.array([0,0])

    def draw(self, street_speed=1):
        """Draws the street to screen according to the current speed"""

        if not self.screen == []:
            self.screen.fill(mycolors.white)
            self.screen.blit(self.lane_image, (0, 100))

            # Fill up the streets:
            for i in range(self.number_of_lanes):
                cycle = int(self.lane_height / street_speed)
                shift_px_y = street_speed * self.t % cycle
                self.screen.blit(self.lane_image, (self.lane_width * i, shift_px_y))
                self.screen.blit(self.lane_image, (self.lane_width * i, -self.lane_height + shift_px_y))

            for agent in self.agent_list:
                agent.draw(self.screen)

    def gameloop(self):
        """All functions needed for one loop cycle"""
        self.tick()
        self.handle_events()
        self.update_positions()
        self.draw()



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

