import pygame
import numpy as np
import mycolors
import random


class TrafficAgents:
    """An object on the street (including the player, enemies and fixed obstacles)

        Attributes:
            lane: current lane, integer, 1-to-1 with position
            _lane_width: lane width in pixels
            _play_area: screen size (width, height)
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

    def __init__(self, play_area, lane_width, starting_lane=1, agent_type='enemy'):
        self.lane = starting_lane
        self._lane_width = lane_width
        self._play_area = play_area
        self.agent_type = agent_type
        if agent_type == 'enemy':
            self.image = pygame.image.load('car_sprite_enemy.png')
            pos_y = -self.image.get_height()
            self.speed = np.array([0, 1])
        else:
            self.image = pygame.image.load('car_sprite.png')
            pos_y = self._play_area[1] - self.image.get_height()
            self.speed = np.array([0, 0])
            if self.agent_type == 'player':
                pass
            elif agent_type == 'qlearner':
                self.qlearner = QLearningHelper()

        self.position = np.array([self.get_pos_x_from_lane(), pos_y])
        self.collision_rect = pygame.Rect((self.position[0], self.position[1]), (self.image.get_width(),
                                                                                 self.image.get_height()))

    def get_pos_x_from_lane(self):
        return self._lane_width * (self.lane - 1) + (self._lane_width - self.image.get_width()) / 2

    def get_lane_from_position(self):
        return int(
            round((self.position[0] - (self._lane_width - self.image.get_width()) / 2) / self._lane_width, 1) + 1)

    def update_position(self, manual_player_speed):
        if self.agent_type == 'player':
            self.speed = manual_player_speed
        elif self.agent_type == 'qlearner':
            self.speed = self.qlearner.get_speed()

        new_position = self.position + self.speed

        # integrity check for new position
        if new_position[0] >= 0 and new_position[0] + self.image.get_width() <= self._play_area[0]:
            self.position = new_position
            self.collision_rect.move_ip(self.speed[0], self.speed[1])
            self.lane = self.get_lane_from_position()

        # check if agent cant be deleted
        if new_position[1] > self._play_area[1]:
            return False
        else:
            return True

    def check_collision(self, other_rect):
        return self.collision_rect.colliderect(other_rect.collision_rect)

    def draw(self, surface):
        surface.blit(self.image, (self.position[0], self.position[1]))


class GameSession:
    """ Underlying object which manages all parts of a GameSession

        Attributes:
            game_clock: clock for the game to count the loops
            FPS: 60

            lane_image = 'street_sprite.png'
            lane_width = 100: given by pixels of picture
            lane_height = 500: given by pixels of picture
            lane_position_y: the three y coordinates for the lanes moving up and down

            number_of_lanes: integer
            agent_list: agent[0] is always the player
            man_player_speed: to handle inputs and move the car

            t: number of ticks of the games

            spawning_probability: prob to spawn a new enemy, increasing with time

            req_size: (width, height)
            draw: states if the surface is drawn on screen
            surface: the surface to blit all the images to
            session_id: number of gamesession

            live = True: status of the game, running or not

        Methods:
            tick(self)
            spawn_enemies(self)
            get_list_of_agents_at_lane(self)
            handle_events(self, events)
            update_positions(self)
            check_collision_with_player(self)
            draw_surface(self)
            get_surface(self): returns surface to draw on screen
            end_session(self): sets live to false and reduces number of sessions
            gameloop(self)

    """

    _number_of_sessions = 0
    CLOSE = 100
    MEDIUM = 250
    FAR = 400

    def __init__(self, number_of_lanes=5, lane_sprite='street_sprite_2.png', fps=120, draw=False):
        """ """

        # init game_clock
        self.game_clock = pygame.time.Clock()
        self.FPS = fps

        # load street sprite
        self.lane_image = pygame.image.load(lane_sprite)
        self.lane_height = self.lane_image.get_height()
        self.lane_width = self.lane_image.get_width()
        self.lane_position_y = np.array([0, -self.lane_height, -2 * self.lane_height])

        # init further attributes
        self.number_of_lanes = number_of_lanes
        self.agent_list = []
        self.man_player_speed = np.array([0, 0])
        self.t = 0
        self.spawning_probability = 0

        # init subsurface
        self.req_size = (number_of_lanes * self.lane_width, self.lane_height)
        self.draw = draw
        if self.draw:
            self.surface = pygame.Surface(self.req_size)
            self.session_id = GameSession._number_of_sessions
            GameSession._number_of_sessions += 1
        else:
            self.surface = None

        self.agent_list.append(TrafficAgents(play_area=self.req_size, lane_width=self.lane_width, starting_lane=3,
                                             agent_type='qlearner'))

        self.live = True

    def tick(self):
        self.game_clock.tick(self.FPS)
        self.t += 1

    def spawn_new_enemy(self):
        if np.random.rand() < self.spawning_probability:
            spawn_lane = np.random.randint(1, self.number_of_lanes + 1)

            new_agent = TrafficAgents(play_area=self.req_size, lane_width=self.lane_width, starting_lane=spawn_lane)

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

    def get_max_y_coord_of_agents_at_lane(self, lane, default=0):
        if len(self.agent_list) > 0:
            list_without_player = [agent.position[1] for agent in self.agent_list if agent.lane == lane]
            return max(list_without_player[1:], default=default)
        else:
            return default

    def handle_events(self, events):
        """For events like quit or userinputs"""
        for event in events:
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
                self.man_player_speed = np.array([0, 0])
                

    def get_state(self):
        state = np.zeros(3)
        max_y_diff_surrounding = np.zeros(3)

        for i in range(len(max_y_diff_surrounding)):
            max_y_diff_surrounding[i] = self.get_max_y_coord_of_agents_at_lane(self.agent_list[0].lane-1+i)

        for i in range(len(state)):
            if self.agent_list[0].position[1]-max_y_diff_surrounding[i] <= GameSession.CLOSE:
                state[i] = 2
            if (self.agent_list[0].position[1]-max_y_diff_surrounding[i] > GameSession.CLOSE) and (self.agent_list[0].position[1]-max_y_diff_surrounding[i] <= GameSession.MEDIUM):
                state[i] = 1
            if (self.agent_list[0].position[1]-max_y_diff_surrounding[i] > GameSession.MEDIUM) and (self.agent_list[0].position[1]-max_y_diff_surrounding[i] <= GameSession.FAR):
                state[i] = 0
        if self.agent_list[0].lane == 1:
            state[0] = 3
        if self.agent_list[0].lane == self.number_of_lanes:
            state[2] = 3
        return state

    def check_collisions_with_player(self):
        enemies_at_lane = self.get_list_of_agents_at_lane(self.agent_list[0].lane)
        enemies_at_lane.pop(0)
        if not self.agent_list[0].collision_rect.collidelist(enemies_at_lane) == -1:
            return True
        else:
            return False

    def draw_surface(self, street_speed=4):
        """Draws the street to screen according to the current speed"""

        if self.surface is not None:
            self.surface.fill(mycolors.white)

            # Fill up the streets:
            self.lane_position_y = self.lane_position_y + street_speed
            for i in range(self.number_of_lanes):
                self.surface.blit(self.lane_image, (self.lane_width * i, self.lane_position_y[0]))
                self.surface.blit(self.lane_image, (self.lane_width * i, self.lane_position_y[1]))
                self.surface.blit(self.lane_image, (self.lane_width * i, self.lane_position_y[2]))

            if self.lane_position_y[0] > self.req_size[1]:
                self.lane_position_y[0] = self.lane_position_y[2] - self.lane_height

            if self.lane_position_y[1] > self.req_size[1]:
                self.lane_position_y[1] = self.lane_position_y[0] - self.lane_height

            if self.lane_position_y[2] > self.req_size[1]:
                self.lane_position_y[2] = self.lane_position_y[1] - self.lane_height

            for agent in self.agent_list:
                agent.draw(self.surface)

    def get_surface(self):
        return self.surface

    def end_session(self):
        self.live = False
        if self.draw:
            GameSession._number_of_sessions -= 1

    def gameloop(self, events):
        """All functions needed for one loop cycle"""
        if self.live:
            self.tick()
            self.spawn_new_enemy()
            self.handle_events(events)
            self.update_positions()
            self.draw_surface()
            if self.check_collisions_with_player():
                self.end_session()


class DisplayHelper:
    """Handle the display coordination of several GameSessions

        Attributes:
            screen: pygame display
            surface:
            max_sessions:
            subsurfaces_list:


        Methods:
            set_screen_size(self, new_size)
            init_subsurfaces(self)
            draw_on_screen(self, surface, position)

    """

    def __init__(self, number_of_sessions=1, screen_size=(0, 0)):

        # init pygame
        pygame.init()
        if screen_size[0] == 0 or screen_size[1] == 0:
            if number_of_sessions == 1:
                screen_size = (800, 500)
            else:
                screen_size = (1000, 1000)
        self.screen = None
        self.surface = None
        self.set_screen_size(screen_size)

        self.max_sessions = (2, 2)
        self.subsurfaces_list = []

        self.init_subsurface(number_of_sessions)

    def set_screen_size(self, new_size):
        self.screen = pygame.display.set_mode(new_size)
        self.surface = pygame.display.get_surface()

    def init_subsurface(self, number_of_sessions):

        if number_of_sessions == 1:
            new_subsurface_rect = pygame.Rect((0, 0), (800, 500))
            new_subsurface = self.surface.subsurface(new_subsurface_rect)
            self.subsurfaces_list.append(new_subsurface)
        else:
            for i in range(self.max_sessions[0]):
                for j in range(self.max_sessions[1]):
                    new_subsurface_rect = pygame.Rect((500 * j, 500 * i), (500, 500))
                    new_subsurface = self.surface.subsurface(new_subsurface_rect)
                    self.subsurfaces_list.append(new_subsurface)

        # # Check if any subsurface exists
        # if not self.subsurfaces_list:
        #     new_subsurface_rect = pygame.Rect(self.next_start, req_size)
        #     new_subsurface = self.surface.subsurface(new_subsurface_rect)
        #
        #     self.next_start = (req_size[0], 0)
        #     self.max_height = req_size[1]
        #
        #     # Check if new surface can fit in the first row
        #     elif len(self.subsurfaces_list) <= self.max_sessions[1]:
        #         self.max_height = max(self.max_height, req_size[1])
        #         new_screen_size = (self.screen.get_width() + req_size[0], self.max_height)
        #         self.set_screen_size(new_screen_size)
        #
        #         # if max surfaces in a row is reached set next to next row
        #         if len(self.subsurfaces_list) == self.max_sessions[1]:
        #             self.next_start = (0, self.max_height + 1)
        #         else:
        #             self.next_start = (self.screen.get_width() + 1, 0)
        #
        #     else:
        #         self.next_start = (0, max(500))
        #
        #
        #     self.subsurfaces_list.append(new_subsurface)
        #
        #     return new_subsurface

    def draw_on_screen(self, surface, position):
        if position <= 3:
            self.subsurfaces_list[position].blit(surface, (0, 0))


class QLearningHelper():
    '''
    We create a matrix Q of all (action, state)-pairs. The matrix Q has dimensions 3x4^x with x as the size of the
    localfield. x = 8 for the case of a 3x3 view around the head of the snake.

    Matrix Q:
    First row corresponds to a left turn
    Second row corresponds to the current direction
    Third row corresponds to a right turn


    0 is a free field (grey)
    1 is a border (black)
    2 is a part of the snake (red)
    3 is a cherry (green)

    Idea of state-to-(index of Q) isomorphism:
    We read a state as a number with x digits (row first, then next column)
    -------------
      0 | 0 | 1
    -------------
      3 | H | 1
    -------------
      0 | 2 | 1
    -------------
    In the center there is always the head of the snake. The field is changed such that the current direction of
    the snake is always to the top. The state above has the number 00131021 and corresponds to the index 1865.
    '''
    LEFTTURN = np.array([(0, 1), (-1, 0)])
    RIGHTTURN = np.array([(0, -1), (1, 0)])
    NOTURN = np.array([(1, 0), (0, 1)])

    REWARD_ALIVE = 1
    REWARD_DIE = -100
    REWARD_CHERRY = 1000

    GAMMARATE = 0.9

    # Number of field_types -> Wall, Free, Snake, Cherry
    n_fieldtypes = 4

    def __init__(self, size_of_local_matrix=3, max_random_steps=500):
        self.localmatrix_size = size_of_local_matrix
        self.localmatrix_neighbors = self.localmatrix_size ** 2 - 1
        self.Q = np.zeros((3, QLearningHelper.n_fieldtypes ** self.localmatrix_neighbors))

        if max_random_steps > 0:
            self.max_amount_of_steps_with_random = 500
            self.rand_step = True
        elif max_random_steps == 0:
            self.max_amount_of_steps_with_random = 0
            self.rand_step = False
        elif max_random_steps < 0:
            self.max_amount_of_steps_with_random = -1

        self.amount_of_steps_with_random = 0

        self.old_turn = ()
        self.old_Qindex = -1
        self.new_turn = ()
        self.new_Qindex = -1

    @staticmethod
    def Qindex_to_localfield(Qindex):
        localfield = np.base_repr(Qindex, base=QLearningHelper.n_fieldtypes)
        return localfield

    @staticmethod
    def localfield_to_Qindex(localfield):
        Qindex = np.int(str(localfield), QLearningHelper.n_fieldtypes)
        return Qindex

    @staticmethod
    def convert_color_to_int(color):
        ''' 0 is a free field (grey)
        1 is a border (black)
        2 is a part of the snake (red)
        3 is a cherry (green)
        '''
        if color == mycolors.black:
            code = 1
        elif color == mycolors.red:
            code = 2
        elif color == mycolors.green:
            code = 3
        elif color == mycolors.blue:
            code = -1
        else:
            code = 0
        return code

    @staticmethod
    def get_indexQ(color_matrix, coor_head, direction):
        steps = 1
        start = coor_head - steps
        end = coor_head + steps + 1

        color_matrix_int = list(list(map(QLearningHelper.convert_color_to_int, row)) for row in color_matrix)
        color_matrix_int = np.array(color_matrix_int)
        localmatrix_int = color_matrix_int[start[1]:end[1], start[0]:end[0]]

        if np.array_equal(direction, np.array([1, 0])):
            localmatrix = np.rot90(localmatrix_int)
        elif np.array_equal(direction, np.array([-1, 0])):
            localmatrix = np.rot90(localmatrix_int, 3)
        elif np.array_equal(direction, np.array([0, 1])):
            localmatrix = np.rot90(localmatrix_int, 2)
        elif np.array_equal(direction, np.array([0, -1])):
            localmatrix = localmatrix_int

        indexQ = QLearningHelper.get_indexQ_from_localmatrix(localmatrix)
        return indexQ

    @staticmethod
    def get_indexQ_from_localmatrix(localmatrix):
        localfield_str = ''
        for m in range(np.shape(localmatrix)[0]):
            for n in range(np.shape(localmatrix)[1]):
                if m == n and m == 1:
                    pass
                else:
                    localfield_str += str(localmatrix[m, n])

        index_localmatrix = QLearningHelper.localfield_to_Qindex(localfield_str)
        return index_localmatrix

    def get_speed(self):
        random_number = np.random.randint(0, 3)
        print(random_number)
        if  random_number == 0:
            speed = np.array([-100, 0])
        elif random_number == 1:
            speed = np.array([0,0])
        elif random_number == 2:
            speed = np.array([100, 0])

        return speed

    def get_turn(self, indexQ):
        next_turn = None
        if self.max_amount_of_steps_with_random == -1:
            if random.randint(1, 10) < 2:
                self.rand_step = True
            else:
                self.rand_step = False
            # print(self.rand_step)

        if self.amount_of_steps_with_random < self.max_amount_of_steps_with_random or self.rand_step:
            rnd = random.randint(1, 3)
            if rnd == 1:
                next_turn = QLearningHelper.LEFTTURN
            elif rnd == 3:
                next_turn = QLearningHelper.RIGHTTURN
            else:
                next_turn = QLearningHelper.NOTURN
            self.amount_of_steps_with_random += 1
            # print('random step')
        else:
            q_values = self.Q[:, indexQ]
            #print(q_values)
            arg_max = np.argmax(q_values)

            if arg_max == 0:
                next_turn = QLearningHelper.LEFTTURN
            elif arg_max == 1:
                next_turn = QLearningHelper.NOTURN
            elif arg_max == 2:
                next_turn = QLearningHelper.RIGHTTURN

        return next_turn

    @staticmethod
    def turn_to_int(turn):
        if np.all(turn == QLearningHelper.LEFTTURN):
            x = 0
        elif np.all(turn == QLearningHelper.NOTURN):
            x = 1
        elif np.all(turn == QLearningHelper.RIGHTTURN):
            x = 2
        return x

    def update_Q(self, reward):
        old_action = QLearningHelper.turn_to_int(self.old_turn)
        if reward == -1:
            reward = QLearningHelper.REWARD_DIE
            q_new = reward
        else:
            if reward == None:
                reward = QLearningHelper.REWARD_ALIVE
            elif reward == 1:
                reward = QLearningHelper.REWARD_CHERRY
            q_new = reward + QLearningHelper.GAMMARATE * np.max(self.Q[:, self.new_Qindex])

        self.Q[old_action, self.old_Qindex] = q_new
        # print(q_new)

    def save(self, filename):
        ''' Saves a numpy array into a file with .npy ending'''
        np.save(filename, self.Q)
        # print('File saved')

    def reset(self, filename):
        self.Q = np.zeros((3, QLearningHelper.n_fieldtypes ** self.localmatrix_neighbors))
        self.save(filename)
        #print('File reset')

    def load(self, filename):
        ''' Loads a numpy array from a .npy file'''

        if filename[-4::1] == '.npy':
            self.Q = np.load(filename)
        else:
            filename = filename + '.npy'
            self.Q = np.load(filename)
        #print('File loaded')
