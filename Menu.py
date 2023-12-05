# This is a class that will handle option-menu functionality.
# Basically, I want to have the options menu in its own little loop
# with a list variable set to some default parameters when the class is first run
# and maybe a function to run in the menu loop... basically, we gotta cover our options so we
# havve a default set for if the menu is never entered and then a list that returns some stuff for if
# they do... there's going to be a list either way. But, you know

import pygame

from car import Car
from track import Track


class Menu:
    # I wonder if it will let us put cars up here
    __CAR_SELECTION = [
        Car(80, 70, 0.5, "imgs/vehicles/Ambulance.png"),
        Car(100, 40, 0.7, "imgs/vehicles/Audi.png"),
        Car(120, 30, 0.4, "imgs/vehicles/Black_viper.png"),
        Car(100, 40, 0.5, "imgs/vehicles/Car.png"),
        Car(75, 60, 0.8, "imgs/vehicles/Mini_truck.png"),
        Car(75, 60, 0.6, "imgs/vehicles/Mini_van.png"),
        Car(120, 50, 0.5, "imgs/vehicles/Police.png"),
        Car(88, 40, 0.7, "imgs/vehicles/taxi.png"),
        Car(65, 70, 0.25, "imgs/vehicles/truck.png")
    ]

    __ROAD_SELECTION = [
        Track(1, 1),
        Track(0.8, 0.8, (210, 180, 140),
              (20, 124, 4), (101, 67, 33)),
        Track(1.4, 0.5, (6, 209, 225),
              (0, 69, 228), (225, 225, 226))
    ]

    def __init__(self, FPS, window):
        ## Remember to set our default list here. But I think we can get away with not doing that for now
        print("Menu class initialized")
        self._FPS = FPS
        self.clock = pygame.time.Clock()
        self.__WINDOW = window

        self._selectedCar = self.__CAR_SELECTION[1]
        self.__selectedTrack = self.__ROAD_SELECTION[0]
        self.__starterConfig = [self._selectedCar, self.__selectedTrack]

        self._menuRunning = False

    def show_menu(self):

        carsList = ["Ambulance", "Audi", "Viper", "Stang?", "Pickup", "Van", "5-0", "Taxi", "Truck"]
        trackList = ["Pavement", "Dirt", "Ice"]

        ##First we need to do our initial background
        menuBackground = pygame.image.load('imgs/abstract1.png')
        menuBackground = pygame.transform.scale(menuBackground, (800, 2000))
        # forgo stretching for now and see where we're at

        # Guess we should setup our font here
        menuTextSurf, menuTextRext = self.text_objects("Options", 75, (0, 0, 0))
        menuTextRext.center = (550, 100)

        carSelectSurf, carSelectRect = self.text_objects("Car Select:", 50, (0, 0, 0))
        carSelectRect.center = (565, 250)

        currentCarSurf, currentCarRect = self.text_objects("Current selection:", 30, (0, 0, 0))
        currentCarRect.center = (565, 600)

        trackLabelSurf, trackLabelRect = self.text_objects("Track Select:", 30, (255, 255, 255))
        trackLabelRect.center = (175, 250)

        currentTrackSurf, currentTrackRect = self.text_objects("Current selection:", 30, (255, 255, 255))
        currentTrackRect.center = (175, 550)



        print("Actual menu loop")

        self._menuRunning = True

        while self._menuRunning:

            ##Since this one updates, it needs to go inside of the running loop
            carSelectionSurf, carSelectionRect = self.text_objects(
                f"{carsList[self.__CAR_SELECTION.index(self._selectedCar)]}", 30, (0, 0, 0))
            carSelectionRect.center = (565, 650)
            trackSelectionSurf, trackSelectionRect = self.text_objects(
                f"{trackList[self.__ROAD_SELECTION.index(self.__selectedTrack)]}", 30, (255, 255, 255))
            trackSelectionRect.center = (175, 600)

            self.clock.tick(self._FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Basic quit condition
                    pygame.quit()
                    quit()
                    sys.exit()

            # Title and background drawn in here
            self.__WINDOW.blit(menuBackground, (0, 0))
            self.__WINDOW.blit(menuTextSurf, menuTextRext)

            ##Supplementary labels and such
            self.__WINDOW.blit(carSelectSurf, carSelectRect)
            self.__WINDOW.blit(currentCarSurf, currentCarRect)
            self.__WINDOW.blit(carSelectionSurf, carSelectionRect)

            # This should add in our car buttons
            self.image_button(self.__CAR_SELECTION[0].getImagePath, 51, 112, 560, 295, 0)  # ambulance
            self.image_button(self.__CAR_SELECTION[1].getImagePath, 51, 112, 470, 300, 1)  # audi
            self.image_button(self.__CAR_SELECTION[2].getImagePath, 51, 112, 470, 450, 2)  # viper
            self.image_button(self.__CAR_SELECTION[3].getImagePath, 51, 112, 650, 295, 3)  # mustang?
            self.image_button(self.__CAR_SELECTION[4].getImagePath, 51, 112, 560, 450, 4)  # mini truck
            self.image_button(self.__CAR_SELECTION[5].getImagePath, 51, 112, 650, 450, 5)  # van
            self.image_button(self.__CAR_SELECTION[6].getImagePath, 51, 112, 380, 305, 6)  # police car
            self.image_button(self.__CAR_SELECTION[7].getImagePath, 51, 112, 380, 450, 7)  # taxi
            self.image_button(self.__CAR_SELECTION[8].getImagePath, 51, 112, 740, 300, 8)

            ### Left-side Stuff ###

            # Originally, I was going to allow for a starting weapon selection and a track selection.
            # But the more I think about it, the more I think I just want there to be track selection and that's it
            self.menu_button("PAVEMENT", 150, 50, 100, 300, (128, 128, 128),
                             (158, 158, 158), "pavement")
            self.menu_button("DIRT", 150, 50, 100, 375,
                             (210, 180, 140), (255, 180, 140), "dirt")
            self.menu_button("ICE", 150, 50, 100, 450,
                             (6, 239, 255), (6, 210, 225), "ice")
            self.menu_button("OK", 150, 50, 500, 700, (0, 185, 37),
                             (15, 246, 61), "ok")
            self.menu_button("BACK", 150, 50, 100, 700,
                             (204, 0, 0), (255, 51, 51), "back")

            # Stuff for the labels pertaining to the trackselect
            self.__WINDOW.blit(trackLabelSurf, trackLabelRect)
            self.__WINDOW.blit(currentTrackSurf, currentTrackRect)
            self.__WINDOW.blit(trackSelectionSurf, trackSelectionRect)


    # Seems like it might be easier to give us our own button function over here rather than
    # trying to make the button function from our game class fit the mould here
    def menu_button(self, message, w, h, x, y, iColor, aColor, action=None):
        # print("Menu button pressed")
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        buttonTextSurf, buttonTextRect = self.text_objects(message, 20, (0, 0, 0))

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1 and action != None:
                pygame.draw.rect(self.__WINDOW, aColor, (x+4, y+4, w-2, h-2))
                #print("Button clicked, I guess")  # Got a little ahead of ourselves here
                match (action):
                    case "pavement":
                        print("Pavement pressed")
                        self.__selectedTrack = self.__ROAD_SELECTION[0]
                    case "dirt":
                        print("Dirt button pressed")
                        self.__selectedTrack = self.__ROAD_SELECTION[1]
                    case "ice":
                        print("Ice pressed")
                        self.__selectedTrack = self.__ROAD_SELECTION[2]
                    case "ok":
                        print("OK pressed")
                        self.__starterConfig = [self._selectedCar, self.__selectedTrack]
                        self._menuRunning = False
                    case "back":
                        print("Back pressed")
                        self._menuRunning = False
                    case _:
                        print("Theoretically unreachable")
                buttonTextRect.center = ((x + w / 2 +2), (y + h / 2 + 2))
            else:
                pygame.draw.rect(self.__WINDOW, aColor, (x, y, w, h))
                buttonTextRect.center = ((x + w / 2), (y + h / 2))

        else:
            pygame.draw.rect(self.__WINDOW, iColor, (x, y, w, h))
            buttonTextRect.center = ((x + w/2), (y + h/2))
        self.__WINDOW.blit(buttonTextSurf, buttonTextRect)




    # Also seems like splitting off this functionality and creating a dedicated function for image_buttons
    # would be wise here
    def image_button(self, imagePath, w, h, x, y, action=None):
        # print("Image button pressed")

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        img = pygame.image.load(imagePath)
        # imgRect = img.get_bounding_rect()
        # trimmedSurface = pygame.Surface(imgRect.size)
        # trimmedSurface.blit(img, (0,0), imgRect)

        if x + w > mouse[0] > x and y + h > mouse[1] > y:

            # make the one that the cursor is hovering over slightly bigger... why not?
            img = pygame.transform.scale(img, (w + 4, h + 4))

            if click[0] == 1 and action is not None:
                if isinstance(action, int):
                    self._selectedCar = self.__CAR_SELECTION[action]
                    print(f"Button {action} clicked")
                    self.__WINDOW.blit(img, (x, y))
            else:
                self.__WINDOW.blit(img, (x - 2, y - 2))


        else:
            img = pygame.transform.scale(img, (w, h))
            self.__WINDOW.blit(img, (x, y))

    # Maybe we'll make a separate utils function so that we aren't having to rewrite this function multiple times...
    def text_objects(self, text, size, color):
        TextFont = pygame.font.Font('freesansbold.ttf', size)
        textSurface = TextFont.render(text, True,
                                      color)  # might come back and make the color purely a local thing... idk
        return textSurface, textSurface.get_rect()


    def getStarterOptions(self):
        return self.__starterConfig

    @property
    def getCarsList(self):
        return self.__CAR_SELECTION