import pygame

class Enemy:
    """
    Klasse der Hindernisse
    """
    def __init__(self, starting_lane=3, image='car_enemy.png', street_width = 100, speed_delta_px_per_tick = 1):
        self.lane=starting_lane
        self._image_filename = image
        self._street_width = street_width
        self._delta_px_per_tick = speed_delta_px_per_tick
        if image != '':
            self.image=pygame.image.load(image)
            self.image_width = 60
            self.image_height =100
            self.pos_y_puffer_px = self.image_height
        self.pos_x = 20 + (self.lane-1)*self._street_width
        self.pos_y = -self.pos_y_puffer_px

    def update_position(self):
        self.pos_y +=self._delta_px_per_tick