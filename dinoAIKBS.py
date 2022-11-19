import math

import pygame
import os
import random
import numpy as np
import time
from sys import exit
from experta import *


pygame.init()

# Valid values: HUMAN_MODE or AI_MODE
GAME_MODE = "AI_MODE"

# Valid values
# - "Black"
# - "Blue"
# - "Green"
# - "Orange"
# - "Pink"
# - "Purple"
# - "Red"
# Escolhe a cor do dino
COLOR = input("Insira a cor do Dino que você deseja: \n - Black \n - Blue \n - Green \n - Orange \n - Pink \n - Purple \n - Red\nCor: ")
COLOR = COLOR.capitalize()
DINO_DIR = f"Assets/Dinofy/Dino{COLOR}"

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join(DINO_DIR, "DinoRun1.png")),
           pygame.image.load(os.path.join(DINO_DIR, "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join(DINO_DIR, "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join(DINO_DIR, "DinoDuck1.png")),
           pygame.image.load(os.path.join(DINO_DIR, "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus4.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 90
    Y_POS = 330
    Y_POS_DUCK = 355
    JUMP_VEL = 17
    JUMP_GRAV = 1.1

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = 0
        self.jump_grav = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck and not self.dino_jump:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput == "K_UP" and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == "K_DOWN" and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif userInput == "K_DOWN":
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput == "K_DOWN"):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_duck:
            self.jump_grav = self.JUMP_GRAV * 4
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel
            self.jump_vel -= self.jump_grav
        if self.dino_rect.y > self.Y_POS + 10:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.jump_grav = self.JUMP_GRAV
            self.dino_rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def getXY(self):
        return (self.dino_rect.x, self.dino_rect.y)

    def getJumpVel(self):
        return self.jump_vel


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle():
    def __init__(self, image, type):
        super().__init__()
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()

        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < - self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def getXY(self):
        return (self.rect.x, self.rect.y)

    def getHeight(self):
        return self.rect.y

    def getType(self):
        return (self.type)

    def getWidth(self):
        return self.rect.width


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 345


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)

        # High, middle or ground
        if random.randint(0, 3) == 0:
            self.rect.y = 345
        elif random.randint(0, 2) == 0:
            self.rect.y = 260
        else:
            self.rect.y = 300
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1

class KeyClassifier:
    def __init__(self, state):
        pass

    def keySelector(self, distance, obHeight, speed, obType):
        pass

    def updateState(self, state):
        pass

class ProfessorRuleBasedPlayer(KnowledgeEngine):

    def setAction(self, action):
        self.action = action

    def getAction(self):
        return self.action

    @Rule(AND(Fact(speed=P(lambda x: x < 15)),
              Fact(distance=P(lambda x: x < 300)),
              NOT(Fact(action='K_DOWN'))))
    def jumpSlow(self):
        self.retract(1)
        self.declare(Fact(action='K_UP'))

    @Rule(AND(Fact(speed=P(lambda x: x >= 15 and x < 17)),
              Fact(distance=P(lambda x: x < 400)),
              NOT(Fact(action='K_DOWN'))))
    def jumpFast(self):
        self.retract(1)
        self.declare(Fact(action='K_UP'))

    @Rule(AND(Fact(speed=P(lambda x: x >= 17)),
              Fact(distance=P(lambda x: x < 500)),
              NOT(Fact(action='K_DOWN'))))
    def jumpVeryFast(self):
        self.retract(1)
        self.declare(Fact(action='K_UP'))

    @Rule(AND(Fact(obType=P(lambda x: isinstance(x, Bird))),
              Fact(obHeight=P(lambda x: x > 50))))
    def getDown(self):
        self.retract(1)
        self.declare(Fact(action='K_DOWN'))

    @Rule(Fact(action=MATCH.action))
    def selectAction(self, action):
        self.setAction(action)

class Number(Fact):
    num = Field(int, mandatory=True)

class RuleBasedPlayer(KnowledgeEngine):

    def setAction(self, action):
        self.action = action

    def getAction(self):
        # print(f"act: {self.action}")
        return self.action

    @Rule(AND(Fact(obType=P(lambda x: isinstance(x, Bird))),
              Fact(obHeight=P(lambda x: x < 340))))
    def getDown(self):
        self.retract(self.facts.last_index-1)
        self.declare(Fact(action='K_DOWN'))

    @Rule(Fact(dinoHeight=P(lambda x: x < 330)),
          Fact(distance=MATCH.distance),
          Fact(speed=MATCH.speed),
          Fact(jumpVel=MATCH.jumpVel),
          TEST(lambda distance, speed, jumpVel: distance-2*speed <= 2*speed and jumpVel < 0))
    def fallFast(self):
        self.retract(self.facts.last_index-1)
        self.declare(Fact(action="K_DOWN"))

    def higher(distance, obHeight, speed, obWidth):
        y_jump = [330, 313, 297, 282, 268, 255, 243, 232, 222, 213, 205, 199, 194, 190, 187, 185, 184, 184, 185, 187, 190, 194, 199, 205, 213, 222, 232, 243, 255, 268, 282, 297, 313, 330]

        fall_front = math.floor(distance/speed)
        fall_back = math.ceil((distance+obWidth)/speed)
        if distance < 0:
            return False
        if fall_front > len(y_jump)-1 or fall_back > len(y_jump)-1:
            return False
        # print(f"--> if {y_jump[fall_front] } and {y_jump[fall_back]} < {obHeight}")
        return y_jump[fall_front] < obHeight and \
                y_jump[fall_back] < obHeight

    @Rule(Fact(distance=MATCH.distance),
          Fact(speed=MATCH.speed),
          Fact(obHeight=MATCH.obHeight),
          Fact(obWidth=MATCH.obWidth),
          AND(TEST(higher),
              NOT(Fact(action='K_DOWN'),
              NOT(Fact(action='K_UP')))))
    def jump(self):
        # print("\033[91mJUMP\033[0m")
        self.retract(self.facts.last_index-1)
        self.declare(Fact(action='K_UP'))

    @Rule(AND(Fact(speed=P(lambda x: x < 15)),
              Fact(distance=P(lambda x: x > 80 and x < 300)),
              NOT(Fact(action='K_DOWN'))))
    def jumpSlow(self):
           self.retract(1)
           self.declare(Fact(action='K_UP'))

    @Rule(AND(Fact(speed=P(lambda x: x >= 15 and x < 17)),
              Fact(distance=P(lambda x: x < 400)),
              NOT(Fact(action='K_DOWN'))))
    def jumpFast(self):
           self.retract(1)
           self.declare(Fact(action='K_UP'))

    @Rule(AND(Fact(speed=P(lambda x: x >= 17)),
              Fact(distance=P(lambda x: x < 500)),
              NOT(Fact(action='K_DOWN'))))
    def jumpVeryFast(self):
           self.retract(1)
           self.declare(Fact(action='K_UP'))

    @Rule(Fact(action=MATCH.action))
    def selectAction(self, action):
        self.setAction(action)

class RuleBasedKeyClassifier(KeyClassifier):
    def __init__(self):
        self.engine = RuleBasedPlayer()

    def keySelector(self, dist, obH, sp, obT, y, obW, jv):
        self.engine.reset()
        self.engine.declare(Fact(distance=dist))
        self.engine.declare(Fact(obHeight=obH))
        self.engine.declare(Fact(speed=sp))
        self.engine.declare(Fact(obType=obT))
        self.engine.declare(Fact(dinoHeight=y))
        self.engine.declare(Fact(obWidth=obW))
        self.engine.declare(Fact(jumpVel=jv))
        self.engine.declare(Fact(action='K_NO'))
        self.engine.run()
        return self.engine.getAction()



def playerKeySelector():
    userInputArray = pygame.key.get_pressed()
    if userInputArray[pygame.K_UP]:
        return "K_UP"
    elif userInputArray[pygame.K_DOWN]:
        return "K_DOWN"
    else:
        return "K_NO"

def playGame():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 383
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    spawn_dist = 0

    def score():
        global points, game_speed
        points += 0.25
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(int(points)), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        SCREEN.fill((255, 255, 255))

        distance = 1500
        obHeight = 0
        obType = 2
        obWidth = 0
        if len(obstacles) != 0:
            xy = obstacles[0].getXY()
            distance = xy[0]
            obHeight = obstacles[0].getHeight()
            obType = obstacles[0]
            obWidth = obstacles[0].getWidth()

        if GAME_MODE == "HUMAN_MODE":
            userInput = playerKeySelector()
        else:
            x, y = player.getXY()
            jv = player.getJumpVel()
            userInput = aiPlayer.keySelector(distance, obHeight, game_speed, obType, y, obWidth, jv)

        if len(obstacles) == 0 or obstacles[-1].getXY()[0] < spawn_dist:
            spawn_dist = random.randint(0, 670)
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 5) == 5:
                obstacles.append(Bird(BIRD))

        player.update(userInput)
        player.draw(SCREEN)

        for obstacle in list(obstacles):
            obstacle.update()
            obstacle.draw(SCREEN)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(60)
        pygame.display.update()

        for obstacle in obstacles:
            if player.dino_rect.colliderect(obstacle.rect):
                print (game_speed, distance)
                pygame.time.delay(2000)
                death_count += 1
                return points

if __name__ == "__main__":
    global aiPlayer
    aiPlayer = RuleBasedKeyClassifier()
    playGame()

