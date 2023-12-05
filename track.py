import  pygame

class Track:

    def __init__(self, tractionCoefficient, speedCoefficient, roadColor=(128, 128, 128),
                lineColor=(255, 255, 255), edgeColor=(0,204,0)):
        self.__roadColor = roadColor
        self.__lineColor = lineColor
        self.__edgeColor = edgeColor
        self.__tractionCoefficient = tractionCoefficient
        self.__speedCoefficient = speedCoefficient

    @property
    def roadColor(self):
        return self.__roadColor

    @property
    def lineColor(self):
        return self.__lineColor

    @property
    def edgeColor(self):
        return self.__edgeColor

    @property
    def tractionCoefficient(self):
        return self.__tractionCoefficient

    @property
    def speedCoefficient(self):
        return self.__speedCoefficient