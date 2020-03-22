import pygame

class Car:
    """
    Klasse der Autos
    """
    def __init__(self, starting_lane=3, image='car_enemy.png', street_width=100, speed_delta_px_per_tick=1):
        self.lane=starting_lane
        self._image_filename = image
        self._street_width = street_width
        self._delta_px_per_tick = speed_delta_px_per_tick
        if image != '':
            self.image = pygame.image.load(image)
            self.image_width = 60
            self.image_height = 100
            self.pos_y_puffer_px = self.image_height
        self.pos_x = 20 + (self.lane-1)*self._street_width
        self.pos_y = 0

    def update_position(self):
        self.pos_y +=self._delta_px_per_tick

class MyCar(Car):
    """Car controlled by user"""
    def __init__(self,starting_lane=1,image='street_sprite.png', street_width=100):
        super().__init__(starting_lane,image,street_width=100)

    def update_x(self):
        self.pos_x = 20 + (self.lane-1)*self._street_width

class Enemy(Car):
    """Class of obstacle cars"""
    def __init__(self,starting_lane,image,street_width=100,speed_delta_px_per_tick=1):
        super().__init__(starting_lane,image,street_width=100,speed_delta_px_per_tick=1)
        self.pos_y = -self.pos_y_puffer_px