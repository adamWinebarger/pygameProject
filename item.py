import pygame

from enum import Enum

class ItemType(Enum):
    HEALTH = 0
    BOMB = 1
    SHIELD = 2
    BOOST = 3



class Item(pygame.sprite.Sprite):

    def __init__(self, imagePath, itemType, x, y):
        pygame.sprite.Sprite.__init__(self)

        self._image = pygame.image.load(imagePath)
        self._image = pygame.transform.scale(self._image, (36, 36))
        self._itemType = itemType
        self._x = x
        self._y = y
        self._rect = self._image.get_rect()
        self._rect.center = [self._x,self._y]



    @property
    def image(self):
        return self._image

    @property
    def itemType(self):
        return self._itemType

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, val):
        self._rect = val