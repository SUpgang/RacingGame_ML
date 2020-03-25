import pygame
import numpy as np
import mycolors


class TrafficAgents:
    """An object on the street (including the player, enemies and fixed obstacles)

        Attributes:
            lane: current lane, integer, 1-to-1 with position
            _lane_width: lane width in pixels
            _screen_height: screen height in pixels
            _screen_width: screen width in pixels
            agent_type: 'enemy' for enemy car, 'player' for player
            image: pygame image
            position = (pos_x, pos_y): numpy array
            speed = (speed_x, speed_y): numpy array, number of pixel to move every tick
            collision_rect: pygame rect to check for collisions

        Methods:
            get_pos_x_from_lane(self): returns the pos_x according to self.lane
            get_lane_from_position(self): returns lane calculated from the position[0]
            update_position(self, manual_speed)
            check_collision(self, other_rect)
            draw(self)

    """

    def __init__(self, screen_height, screen_width, lane_width, starting_lane=1, agent_type='enemy'):
        self.lane = starting_lane
        self._lane_width = lane_width
        self._screen_height = screen_height
        self._screen_width = screen_width
        self.agent_type = agent_type
        if agent_type == 'player':
            self.image = pygame.image.load('car_sprite.png')
            pos_y = screen_height-self.image.get_height()
            speed_x = 0
            speed_y = 0
        else:
            self.image = pygame.image.load('car_sprite_enemy.png')
            pos_y = -self.image.get_height()
            speed_x = 0
            speed_y = 1
        self.position = np.array([self.get_pos_x_from_lane(),pos_y])
        self.speed = np.array([speed_x,speed_y])
        self.collision_rect = pygame.Rect((self.position[0], self.position[1]), (self.image.get_width(),
                                                                                 self.image.get_height()))

    def get_pos_x_from_lane(self):
        return self._lane_width * (self.lane - 1) + (self._lane_width - self.image.get_width()) / 2

    def get_lane_from_position(self):
        return int(round((self.position[0] - (self._lane_width - self.image.get_width()) / 2 ) / self._lane_width, 1)+1)

    def update_position(self, manual_player_speed):
        if self.agent_type == 'player':
            self.speed = manual_player_speed

        new_position = self.position + self.speed

        # integrity check for new position
        if new_position[0] >= 0 and new_position[0] + self.image.get_width() <= self._screen_width:
            self.position = new_position
            self.collision_rect.move_ip(self.speed[0], self.speed[1])
            self.lane = self.get_lane_from_position()

        # check if agent cant be deleted
        if new_position[1] > self._screen_height:
            return False
        else:
            return True

    def check_collision(self, other_rect):
        return self.collision_rect.colliderect(other_rect.collision_rect)

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1]))
        

class GameSession:
    """ Underlying object which manages all parts of a GameSession

        Attributes:
            game_clock: clock for the game to count the loops
            FPS: 60
            screen

            lane_image = 'street_sprite.png'
            lane_width = 100: given by pixels of picture
            lane_height = 500: given by pixels of picture

            number_of_lanes: integer
            agent_list: agent[0] is always the player
            man_player_speed: to handle inputs and move the car

            t: number of ticks of the games

            spawning_probability: prob to spawn a new enemy, increasing with time

            req_screen_height: requiered screen height
            req_screen_width: requiered screen width

            live = True: status of the game, running or not

        Methods:
            tick(self)
            handle_events(self)
            update_positions(self)
            draw(self)
            gameloop(self)

    """

    def __init__(self, player_type = 'manual', number_of_lanes=8, lane_sprite='street_sprite.png', fps=120, screen=[]):
        """ """

        # init game_clock
        self.game_clock = pygame.time.Clock()
        self.FPS = fps
        self.screen = screen

        # load street sprite
        self.lane_image = pygame.image.load(lane_sprite)
        self.lane_height = self.lane_image.get_height()
        self.lane_width = self.lane_image.get_width()
        self.lane_position_y = np.array([0, -self.lane_height, -2*self.lane_height])

        # init further attributes
        self.number_of_lanes = number_of_lanes
        self.agent_list = []
        self.man_player_speed = np.array([0,0])
        self.t = 0
        self.spawning_probability = 0

        # init screen
        self.req_screen_height = self.lane_height
        self.req_screen_width = number_of_lanes * self.lane_width
        if not screen == []:
            self.screen = pygame.display.set_mode((self.req_screen_width, self.req_screen_height))

        self.agent_list.append(TrafficAgents(screen_height=self.req_screen_height, screen_width=self.req_screen_width,
                                             lane_width=self.lane_width, starting_lane=3, agent_type='player'))
        self.live = True

    def tick(self):
        self.game_clock.tick(self.FPS)
        self.t += 1

    def spawn_new_enemy(self):
        if np.random.rand() < self.spawning_probability:
            spawn_lane = np.random.randint(1, self.number_of_lanes+1)

            new_agent = TrafficAgents(screen_height=self.req_screen_height, screen_width=self.req_screen_width,
                                      lane_width=self.lane_width, starting_lane=spawn_lane)

            agents_at_same_lane_list = self.get_list_of_agents_at_lane(new_agent.lane)

            if new_agent.collision_rect.collidelist(agents_at_same_lane_list) == -1:
                self.agent_list.append(new_agent)
                self.spawning_probability = 0

        else:
            self.spawning_probability += round(1 / ((len(self.agent_list)) * self.FPS * 50), 8)

    def get_list_of_agents_at_lane(self, lane):
        if len(self.agent_list) > 0:
            return [agent.collision_rect for agent in self.agent_list if agent.lane == lane]
        else:
            return []

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
        for i, agent in enumerate(self.agent_list):
            if not agent.update_position(self.man_player_speed):
                self.agent_list.pop(i)
            elif i == 0:
                self.man_player_speed = np.array([0,0])

    def check_collisions_with_player(self):
        enemies_at_lane = self.get_list_of_agents_at_lane(self.agent_list[0].lane)
        enemies_at_lane.pop(0)
        if not self.agent_list[0].collision_rect.collidelist(enemies_at_lane) == -1:
            return True
        else:
            return False

    def draw(self, street_speed=2):
        """Draws the street to screen according to the current speed"""

        if not self.screen == []:
            self.screen.fill(mycolors.white)
            self.screen.blit(self.lane_image, (0, 100))

            # Fill up the streets:
            self.lane_position_y = self.lane_position_y + street_speed
            for i in range(self.number_of_lanes):
                self.screen.blit(self.lane_image, (self.lane_width * i, self.lane_position_y[0]))
                self.screen.blit(self.lane_image, (self.lane_width * i, self.lane_position_y[1]))
                self.screen.blit(self.lane_image, (self.lane_width * i, self.lane_position_y[2]))

            if self.lane_position_y[0] > self.req_screen_height:
                self.lane_position_y[0] = self.lane_position_y[2] - self.lane_height

            if self.lane_position_y[1] > self.req_screen_height:
                self.lane_position_y[1] = self.lane_position_y[0] - self.lane_height

            if self.lane_position_y[2] > self.req_screen_height:
                self.lane_position_y[2] = self.lane_position_y[1] - self.lane_height

            for agent in self.agent_list:
                agent.draw(self.screen)

    def gameloop(self):
        """All functions needed for one loop cycle"""
        self.tick()
        self.spawn_new_enemy()
        self.handle_events()
        self.update_positions()
        self.draw()
        if self.check_collisions_with_player():
            self.live = False