# This will be the file in which our Car class lives
# might also have the child classed of car live here as well... haven't decided yet
import pygame

# At this point, it would probably be smarter to have Car inherit from Pygame.sprite.Sprite.
# But we've got the options menu working and I'm worried it might mess things up on this end.
class Car:

    def __init__(self, carSpeed, startingHealth, traction, image):
        self._carSpeed = carSpeed  # numeric
        self._startingHealth = startingHealth  # numeric
        self._tractionCoefficient = traction  # numeric
        self._image = image  # image path

    def transformImageRect(self):
        self._img = pygame.transform.scale(self._img, (self._rect.width / 2, self._rect.height / 2))
        self._rect = self._img.get_rect()
        self._rect.center = [self._x, self._y]

    # I guess we'll only use getters since I don't think I want these vars to be modifiable after they've been set
    @property
    def carSpeed(self):
        return self._carSpeed

    @property
    def startingHealth(self):
        return self._startingHealth

    @property
    def tractionCoefficient(self):
        return self._tractionCoefficient

    @property
    def getImagePath(self):
        return self._image

class PlayerCar(Car, pygame.sprite.Sprite):

    def __init__(self, carTemplate):
        super().__init__(carSpeed=carTemplate.carSpeed, startingHealth=carTemplate.startingHealth,
                         traction=carTemplate.tractionCoefficient, image=carTemplate.getImagePath)
        pygame.sprite.Sprite.__init__(self)

        self._img = pygame.image.load(carTemplate.getImagePath)
        self._x = 630
        self._y = 650
        self._rect = self._img.get_rect()
        self.transformImageRect()
        self._isAlive = True
        self._currentHealth = carTemplate.startingHealth

    def collision(self):
        self._currentHealth -= 10
        self._isAlive = not self._currentHealth == 0

    def heal(self):
        self._currentHealth = self.startingHealth

    ### Getters & Setters

    @property
    def getHealth(self):
        return self._currentHealth

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
    def rect(self, r):
        self._rect = r

    @property
    def image(self):
        return self._img

    @property
    def isAlive(self):
        return self._isAlive

    @isAlive.setter
    def isAlive(self, alive):
        self._isAlive = alive

# Still thinking about possibly doing an enemy car... not sure yet
class RegularCar(Car, pygame.sprite.Sprite):

    def __init__(self, carTemplate, startingX, startingY):
        super().__init__(carSpeed=carTemplate.carSpeed, traction=carTemplate.tractionCoefficient,
                         startingHealth=carTemplate.startingHealth, image=carTemplate.getImagePath)
        pygame.sprite.Sprite.__init__(self)

        self._img = pygame.image.load(carTemplate.getImagePath)
        # really, the only things we should need from our car class are the image path here. So I guess it's not really
        # a true subclass... oh well
        self._x = startingX
        self._y = startingY
        self._rect = self._img.get_rect()
        self.transformImageRect()

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
    def rect(self, r):
        self._rect = r

    @property
    def image(self):
        return self._img

    @image.setter
    def image(self, image):
        self._img = pygame.image.load(image)
        self._rect = self._img.get_rect()
