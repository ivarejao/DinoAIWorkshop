import pygame
import os

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
DINO_DIR = f"../Assets/Dinofy/Dino{COLOR}"

RUNNING = [pygame.image.load(os.path.join(DINO_DIR, "DinoRun1.png")),
           pygame.image.load(os.path.join(DINO_DIR, "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join(DINO_DIR, "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join(DINO_DIR, "DinoDuck1.png")),
           pygame.image.load(os.path.join(DINO_DIR, "DinoDuck2.png"))]

# Inicia o jogo
pygame.init()

# Valid values: HUMAN_MODE or AI_MODE
GAME_MODE = "AI_MODE"
AI_MODE = 'RB'

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SMALL_CACTUS = [pygame.image.load(os.path.join("../Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("../Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("../Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("../Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("../Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("../Assets/Cactus", "LargeCactus3.png")),
                pygame.image.load(os.path.join("../Assets/Cactus", "LargeCactus4.png"))]

BIRD = [pygame.image.load(os.path.join("../Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("../Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("../Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("../Assets/Other", "Track.png"))


global aiPlayer 
global initial_state_size, coord_size, label_state

global game_speed, x_pos_bg, y_pos_bg, points, obstacles