import random
from Obstacle import *
import constants

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = 1
        super().__init__(image, self.type)
        self.rect.y = 345