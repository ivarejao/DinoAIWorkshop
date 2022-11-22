import random
from Obstacle import *
import constants

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = 2
        super().__init__(image, self.type)
        self.rect.y = 325