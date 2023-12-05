# Adam Winebarger & Dennis Salo
# Assignment 4 or 5: Building a video game in Python using OOP
import random
# This is going to be like a car-racing game of sorts. But also the cars are going to shoot at you.
# Because why not

# Since I'm tired of losing track of things on a fairly big python project, I think that we are going to break out
# our classes into separate files... Maybe
import sys
import pygame
import math

from Menu import Menu
from car import PlayerCar, RegularCar
from track import Track
from item import Item, ItemType

## Actually, on second thought, maybe we won't do a game class
# On third though, maybe we will
class Game:

    #Color instance variables
    __BLACK = (0,0,0)
    __BLUE = (0,0,200)
    __LIGHT_BLUE = (0,0,255)
    __RED = (200, 0, 0)
    __BRIGHT_RED = (255, 0, 0)
    __GREEN = (0, 200, 0)
    __BRIGHT_GREEN = (0, 255, 0)

    def __init__(self):

        pygame.init()

        # Font instance variables... need to be after pygame.init
        self.__smallFont = pygame.font.Font("freesansbold.ttf", 20)
        self.__medFont = pygame.font.Font("freesansbold.ttf", 50)
        self.__bigFont = pygame.font.Font("freesansbold.ttf", 75)

        ## Setting initial parameters/values for our screen
        HEIGHT = 800
        WIDTH = 800

        screen_size = (WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('Regular Cars (working title)')

        self.FPS = 120
        self.running = True

        ## Gotta set up our defaults for our menu class
        self.__MENU = Menu(self.FPS, self.screen)
        self.__startingOptions = self.__MENU.getStarterOptions()

        self.clock = pygame.time.Clock()
        pygame.display.update()

        self.intro_loop()
        #self.game_loop()

        pygame.quit()

    def intro_loop(self):

        #This is where we'll do initial setup for our menu background image
        menuBackground = pygame.image.load('imgs/background2.jpg')
        menuBackground = pygame.transform.scale(menuBackground, (800, 1000))

        #Setting up the font stuff for our title text... might actually move this out and make it an instance var
        # idk yet
        titleTextFont = pygame.font.Font('freesansbold.ttf', 100)
        titleTextSurf, titleTextRect = self.text_objects("Regular Cars", titleTextFont)
        titleTextRect.center = (400, 150)

        subtitleTextSurf, subtitleTextRect = self.text_objects("(A working title)", self.__medFont)
        subtitleTextRect.center = (400, 250)

        print("intro loop")

        ## So this is our basic running/core loop
        while self.running:
            self.clock.tick(self.FPS)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Basic quit condition
                    self.running = False
                    break

            # and this is where it's loaded onto the screen
            self.screen.blit(menuBackground, (0,0))

            #drawing in our title text guy
            self.screen.blit(titleTextSurf, titleTextRect)
            self.screen.blit(subtitleTextSurf, subtitleTextRect)

            ## Now lets throw our buttons down... I'm going to do the options button first since I want it to be centered
            # and then I can pivot my buttons off of that
            self.button("OPTIONS", 300, 650, 200, 50, self.__BLUE, self.__LIGHT_BLUE, "menu")

            self.button("PLAY", 33, 575, 200, 50, self.__RED, self.__BRIGHT_RED, "play")
            self.button("QUIT", 567, 575, 200, 50, self.__GREEN, self.__BRIGHT_GREEN, "quit")



    def menu_loop(self):
        print("Menu Loop")
        self.__MENU.show_menu()
        #Get what we need from here
        #self.intro_loop()
        self.__startingOptions = self.__MENU.getStarterOptions()



    def game_loop(self):
        itemsList = {ItemType.HEALTH : 'imgs/powerups/heart.png', ItemType.BOMB : 'imgs/powerups/bomb.png',
                     ItemType.BOOST : 'imgs/powerups/nos.png', ItemType.SHIELD : 'imgs/powerups/shield.png'}
        print("Game Loop")
        track = self.__startingOptions[1]
        w = 'w'
        h = 'h' #mostly just want to do this to make the key-value pair easier
        marker = {w : 20, h : 100}
        distance = 0
        possibleSpawns = [150, 250, 350, 450, 550, 650] #Possible x values for our carSpawns

        spawnableLanes = [0, 0, 0, 0, 0, 0] #Basically, we'll add 120 to this any time a car is spawned in a lane and then
            # have it decrement through every tick of the clock here

        crash = pygame.image.load('imgs/crash.png')
        crash_rect = crash.get_rect()

        score = 0
        invincibleFrames = 0
        boostValue = 0
        boostTime = 0
        antiBoost = 0

        #Gotta make sprite groups apparently
        player_group = pygame.sprite.Group()
        playerCar = PlayerCar(self.__startingOptions[0])
        player_group.add(playerCar)

        vehicleFroup = pygame.sprite.Group()
        difficulty = 3

        itemGroup = pygame.sprite.Group()

        while playerCar.isAlive:

            self.clock.tick(self.FPS)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    sys.exit()

            # Key press events
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                if playerCar.rect.x >= 95:
                    playerCar.rect.x -= 5 * playerCar.tractionCoefficient * track.tractionCoefficient
            if keys[pygame.K_d]:
                if playerCar.rect.x <= 650:
                    playerCar.rect.x += 5 * playerCar.tractionCoefficient * track.tractionCoefficient

            if keys[pygame.K_w]:
                if playerCar.rect.y >= 10:
                    playerCar.rect.y -= 5 * (playerCar.carSpeed / 100) * track.speedCoefficient
            if keys[pygame.K_s]:
                if playerCar.rect.y <= 675:
                    playerCar.rect.y += 5 * (playerCar.carSpeed / 100) * track.speedCoefficient

            if not keys[pygame.K_a] and playerCar.rect.y < 675:
                playerCar.rect.y += 1

            ## I guess let's handle our initial drawing here and see where we're at
            #self.screen.fill(track.edgeColor)
            pygame.draw.rect(self.screen, track.edgeColor, (0, 0, 800, 800))
            pygame.draw.rect(self.screen, track.roadColor, (100, 0, 600, 800))
            #print("In the loop")

            #Going to need to do a bit of logic for the road lines
            distance += 1#playerCar.carSpeed * track.speedCoefficient * .01
            for i in range(0, 5):
                for j in range(marker[h] * -2, marker[h] * 2):
                    pygame.draw.rect(self.screen, track.lineColor, (190 + i * 100, marker[h]+  j * 200 + distance * difficulty % 1600,marker[w], marker[h]))

            #pygame.draw.rect(self.screen, (0,0,0), (100, 100, 95, 25))
            #pygame.draw.rect(self.screen, (0,0,0), ())


            ##Alright, now let's spawn the cars here
            lane = random.randint(0,5)
            if spawnableLanes[lane] == 0:
                spawnVal = random.randint(0, 1000 - difficulty * 2) #This oughta make things interesting
                #print(spawnVal)
                if spawnVal < 30:
                    newNPCCar = RegularCar(random.choice(self.__MENU.getCarsList),
                                           possibleSpawns[lane] + random.randint(-10, 10),
                                           -200)  # This should spawn a car just off screen and then we can move it down

                    vehicleFroup.add(newNPCCar)
                    #self.screen.blit(playerCar.image, (400, 400))
                    spawnableLanes[lane] += 240  # This should make it so that a car can't be spawned in a lane for another two seconds
                    # for l in range(0,5):
                    #     spawnableLanes[l] += 120

            #May as well do our item spawning here
            itemSpawnVal = random.randint(0, 10000)

            if itemSpawnVal < 30:
                itemPick = random.randint(0,3)
                print(f"Item spawn: {ItemType(itemPick)} {itemsList[ItemType(itemPick)]}")
                newItem = Item(itemsList[ItemType(itemPick)], itemPick, possibleSpawns[random.randint(0,5)], -200)
                itemGroup.add(newItem)

            ## Scoreboard can go here, i guess
            scoreLabel = self.text_objects("Score:", self.__smallFont)
            scoreLabel[1].center = (750, 150)
            self.screen.blit(scoreLabel[0], scoreLabel[1])

            scoreValueLabel = self.text_objects(str(score), self.__smallFont)
            scoreValueLabel[1].center = (750, 200)
            self.screen.blit(scoreValueLabel[0], scoreValueLabel[1])

            #May as well put our health bar here
            healthLabel = self.text_objects("Health:", self.__smallFont)
            healthLabel[1].center = (750, 250)
            self.screen.blit(healthLabel[0], healthLabel[1])


            # Now we need to make the vehicles move backwards
            # Let's start with a constant backwards move and then go from there

            for vic in vehicleFroup:
                vic.rect.y += difficulty - (vic.carSpeed / 100 * track.speedCoefficient)

                # Now we need to remove them if they go off the screen on the bottom
                if vic.rect.top >= self.screen.get_height():
                    vic.kill()

                    score += 1

            vehicleFroup.draw(self.screen)
            itemGroup.draw(self.screen)

            for i in itemGroup:
                i.rect.y += difficulty + (playerCar.carSpeed / 100 * track.speedCoefficient)

                if pygame.sprite.collide_rect(playerCar, i):
                    match ItemType(i.itemType):
                        case ItemType.HEALTH:
                            print("Health grabbed")
                            playerCar.heal()
                        case ItemType.BOMB:
                            for vics in vehicleFroup:
                                newCrash = pygame.image.load('imgs/crash.png')
                                newRect = newCrash.get_rect()
                                newRect.center = vics.rect.center
                                vics.image = 'imgs/crash.png'
                                vics.rect = newRect
                            invincibleFrames += 240
                            print("Bomb grabbed")
                        case ItemType.SHIELD:
                            print("Shield grabbed")
                            invincibleFrames += 600
                        case ItemType.BOOST:
                            print("Boost grabed")
                            boostValue = 5
                            boostTime = 600
                        case _:
                            print("Nothing happens here")
                    i.kill()

            ## Drawing player_group here I guess
            if not (invincibleFrames > 0 and int(invincibleFrames / 10) % 2 == 0):
                player_group.draw(self.screen)

            ## I guess we can handle collision checking before we go onto vehicle spawning
            for npcVic in vehicleFroup:
                if pygame.sprite.collide_rect(playerCar, npcVic) and invincibleFrames == 0:
                    playerCar.collision()
                    #crash_rect.center = playerCar.rect.center
                    #self.screen.blit(crash, crash_rect)
                    crash_rect.center = npcVic.rect.center
                    npcVic.image = 'imgs/crash.png'
                    npcVic.rect = crash_rect
                    #self.screen.blit(crash, crash_rect)
                    invincibleFrames += 120

                    if not playerCar.isAlive:
                        crash_rect.center = npcVic.rect.center
                        self.screen.blit(crash, crash_rect)
                        crash_rect.center = playerCar.rect.center
                        self.screen.blit(crash, crash_rect)

            # Had to move this here so that it will update after collision
            pygame.draw.rect(self.screen, self.__RED,
                            (710, 275, 80 * (playerCar.getHealth / playerCar.startingHealth), 25))
            #self.screen.blit(playerCar.image, (playerCar.x, playerCar.y))

            #distance += 1

            ### Increasing the difficulty/speeding up the track here
            if int(distance) >= 1600 * (difficulty - 3) and difficulty < 100:
                difficulty += 1
                #difficulty += 1
            #print(difficulty)
            #print(distance)
            #print(playerCar.x)

            ### And I guess here is as good a place as any to decrement our possible spawn lanes
            for lane in range(6):
                if spawnableLanes[lane] > 0:
                    spawnableLanes[lane] -= 1
            #print(spawnableLanes)

            if invincibleFrames > 0:
                invincibleFrames -= 1

            if boostValue > 0 and distance % 200 == 0:
                print("Accelerating")
                if antiBoost > -5:
                    difficulty += 1
                boostValue -= 1
                antiBoost -= 1
                print(boostValue)

            if boostValue == 0 and boostTime > 0:
                print("Peak boost")
                boostTime -= 1

            if boostTime == 0 and antiBoost < 0 and distance % 200 == 0:
                difficulty -= 1
                antiBoost += 1
                print("Decelerating")


        ### I guess we would put our game over logic here
        self.gameOver()
    def gameOver(self):
        #print("You died")

        goRunning = True
        while goRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_y:
                            self.game_loop()
                            goRunning = False
                        case pygame.K_n:
                            goRunning = False
                        case _:
                            print("Gotta have something here I guess")

            #print("You died")
            #Death rectangle
            pygame.draw.rect(self.screen, (225, 0, 0), (200, 100, 400, 200))
            #Header for the "You died text"
            deathHeader = self.text_objects("You died", self.__medFont)
            deathHeader[1].center = (400, 200)
            self.screen.blit(deathHeader[0], deathHeader[1])

            #Label for the continue message
            continueYN = self.text_objects("Continue? [y/n]", self.__smallFont)
            continueYN[1].center = (400, 250)
            self.screen.blit(continueYN[0], continueYN[1])

            pygame.display.update()

    # Basically modularizing buttons for our
    def button(self, message, xPos, yPos, width, height, iColor, aColor, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        ### Actions upon click being inside the specified things for our stuff
        if xPos + width > mouse[0] > xPos and yPos + height > mouse[1] > yPos:
            pygame.draw.rect(self.screen, aColor, (xPos, yPos, width, height))

            if click[0] == 1 and action is not None:
                match (action):
                    case "play":
                        print("Play pressed") #Will put play game function here when time comes
                        self.game_loop()
                        #self.running = False #Might want to make running a local var again
                    case "menu":
                        print("Menu pressed") #Same deal here
                        self.menu_loop()
                    case "quit":
                        pygame.quit()
                        quit()
                        sys.exit()
                    case "pause":
                        print("Pause fired")
                    case "unpause":
                        print("Unpause fires")
                    case _:
                        print("Theoretically unreachable")
        else:
            pygame.draw.rect(self.screen, iColor, (xPos, yPos, width, height))

        textSurf, textRect = self.text_objects(message, self.__smallFont)
        textRect.center = ((xPos + width / 2), (yPos + height / 2))
        self.screen.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.__BLACK) #might come back and make the color purely a local thing... idk
        return textSurface, textSurface.get_rect()

    def blit_rotate(self, image, topLeft, angle):
        rotatedImage = pygame.transform.rotate(image, angle)
        newRect = rotatedImage.get_rect(center=image.get_rect(topleft=topLeft).center)
        #win.blit(rotatedImage,newRect.topleft)
        return (rotatedImage, newRect)


### Driver code ###
# def main():
#     Game()
#
#
# if __name__ == "main":
#     main()

Game()