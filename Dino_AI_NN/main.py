import pygame
import os
import random
import time
from sys import exit

pygame.init()

# Valid values: HUMAN_MODE or AI_MODE
GAME_MODE = "AI_MODE"
TRAIN_MODE = 0

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("../Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("../Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("../Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("../Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("../Assets/Dino", "DinoDuck2.png"))]

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
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

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
        pygame.draw.rect(SCREEN, self.color, (self.dino_rect.x, self.dino_rect.y, self.dino_rect.width, self.dino_rect.height), 2)

    def getXY(self):
        return (self.dino_rect.x, self.dino_rect.y)


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
        return y_pos_bg - self.rect.y

    def getType(self):
        return (self.type)


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
        if TRAIN_MODE == 0:
            if random.randint(0, 3) == 0:
                self.rect.y = 345
            elif random.randint(0, 2) == 0:
                self.rect.y = 260
            else:
                self.rect.y = 300
        else:
            p = random.randint(0, 2)
            if p == 0:
                self.rect.y = 345
            elif p == 1:
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


def playerKeySelector():
    userInputArray = pygame.key.get_pressed()

    if userInputArray[pygame.K_UP]:
        return "K_UP"
    elif userInputArray[pygame.K_DOWN]:
        return "K_DOWN"
    else:
        return "K_NO"


def playGame(population):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    #player = Dinosaur()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)
    
    
    obstacles = []
    players = []
    net_player = []
    solution_fitness = []
    died = []

    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 383
    points = 0
    spawn_dist = 0

    for solution in population:
        players.append(Dinosaur())
        net_player.append(KeyNeuralNet(model,solution))
        solution_fitness.append(0)
        died.append(False)

    def score():
        global points, game_speed
        points += 0.25
        if points % 100 == 0:
            if TRAIN_MODE == 1:
                game_speed += 3
            else:
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

    def statistics():
        text_1 = font.render(f'Dinosaurs Alive:  {str(died.count(False))}', True, (0, 0, 0))
        text_3 = font.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_3, (50, 480))

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()


        SCREEN.fill((255, 255, 255))

        

        #if GAME_MODE == "HUMAN_MODE":
            #userInput = playerKeySelector()
        #else:
            #userInput = aiPlayer.keySelector(distance, obHeight, game_speed, obType)

        if TRAIN_MODE == 0:
            if len(obstacles) == 0 or obstacles[-1].getXY()[0] < spawn_dist:
                spawn_dist = random.randint(0, 670)
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 5) == 5:
                    obstacles.append(Bird(BIRD))
        else:
            if len(obstacles) == 0 or obstacles[-1].getXY()[0] < spawn_dist:
                spawn_dist = random.randint(0, 670)
                e = random.randint(0, 2)
                if e == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif e == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif e == 2:
                    obstacles.append(Bird(BIRD))

        for i, player in enumerate(players):
            if not died[i]:
                distance = 1500
                obHeight = 0
                altitude = 0
                nx_distance = 1500
                if len(obstacles) != 0:
                    xy = obstacles[0].getXY()
                    distance = xy[0]
                    altitude = xy[1]
                    obHeight = obstacles[0].getHeight()

                if len(obstacles) > 1:
                    nx_distance = obstacles[1].getXY()[0]

                dinoHeight = player.getXY()[1]
                userInput = net_player[i].keySelector(distance/1500, obHeight/123, game_speed/100, dinoHeight/355, altitude/345, nx_distance/1500)
                player.update(userInput)
                
                player.draw(SCREEN)

        for obstacle in list(obstacles):
            obstacle.update()
 
            obstacle.draw(SCREEN)
            for i, player in enumerate(players):
                if player.dino_rect.colliderect(obstacle.rect) and died[i] == False:
                    solution_fitness[i] = points
                    died[i] = True
                    
        if False not in died:
            break
        
        
        background()


        cloud.draw(SCREEN)
        statistics()
        score()
        
        cloud.update()
        


        clock.tick(60)
        pygame.display.update()

    return solution_fitness


import numpy as np
import torch
import pygad

class KeyNeuralNet(KeyClassifier):
    def __init__(self, model, solution):
        self.model = model
        self.solution = solution

    def keySelector(self, distance, obHeight, speed,dinoHeight, altitude, nx_distance):
        
        #features ideal* - > speed, distance, obWidth, obHeight, altitude ,dinoHeigth
        data_in = torch.tensor([[distance, obHeight, speed, dinoHeight, altitude, nx_distance]],dtype=torch.float32)
        #print(data_in)
        prediction = pygad.torchga.predict(model=self.model,solution=self.solution,data=data_in)
        action = prediction[0]
        if action[0] > 0.55:
            return "K_UP"        
        
        return "K_DOWN"

def manyPlaysResults(rounds,solutions):
    results = []
    for round in range(rounds):
        results += [playGame(solutions)]
    npResults = np.asarray(results)
    #print(npResults.mean(axis=0))
    return (results, npResults.mean(axis=0) - npResults.std(axis=0))

from neural_net import torch_ga, on_generation, model

def fitness_func(solution,solution_idx):
    global aiPlayer
    aiPlayer = KeyNeuralNet(model,solution)

    return manyPlaysResults(1)[1]


#Paralel Train GA
class PTGA(pygad.GA):

    def __init__(self, num_generations, num_parents_mating, fitness_func, initial_population=None, sol_per_pop=None, num_genes=None, init_range_low=-4, init_range_high=4, gene_type=float, parent_selection_type="sss", keep_parents=-1, K_tournament=3, crossover_type="single_point", crossover_probability=None, mutation_type="random", mutation_probability=None, mutation_by_replacement=False, mutation_percent_genes='default', mutation_num_genes=None, random_mutation_min_val=-1, random_mutation_max_val=1, gene_space=None, allow_duplicate_genes=True, on_start=None, on_fitness=None, on_parents=None, on_crossover=None, on_mutation=None, callback_generation=None, on_generation=None, on_stop=None, delay_after_gen=0, save_best_solutions=False, save_solutions=False, suppress_warnings=False, stop_criteria=None, parallel_processing=None):
        super().__init__(num_generations, num_parents_mating, fitness_func, initial_population, sol_per_pop, num_genes, init_range_low, init_range_high, gene_type, parent_selection_type, keep_parents, K_tournament, crossover_type, crossover_probability, mutation_type, mutation_probability, mutation_by_replacement, mutation_percent_genes, mutation_num_genes, random_mutation_min_val, random_mutation_max_val, gene_space, allow_duplicate_genes, on_start, on_fitness, on_parents, on_crossover, on_mutation, callback_generation, on_generation, on_stop, delay_after_gen, save_best_solutions, save_solutions, suppress_warnings, stop_criteria, parallel_processing)
        self.my_best = 0
        self.best_score = 0

    def cal_pop_fitness(self):

        #pop_fitness = playGame(self.population)
        pop_fitness = manyPlaysResults(3,self.population)[1]
        #print(pop_fitness)
        max = 0
        max_id = 0
        for i, _ in enumerate(pop_fitness):
            if pop_fitness[i] > max:
                max = pop_fitness[i]
                max_id = i
        
        if max > self.best_score:
            print(f"Saving {max}")
            self.my_best = self.population[max_id]
            torch.save(self.my_best,'best_sol')
            self.best_score = max

        return pop_fitness
    
    def get_top(self):
        return self.my_best,self.best_score


import matplotlib.pyplot as plt



def train(init_sol = None):
    global aiPlayer

    file = open("generations.txt",mode='w') #resetar o arquivo
    file.close()

    if init_sol == None:
        init_pop = torch_ga.population_weights
    else:
        init_sol = torch.load(init_sol)
        init_pop = [init_sol for i in range(50)]

    ga_instance = PTGA(num_generations=1200,
                            num_parents_mating=2,
                            initial_population=init_pop,
                            fitness_func=fitness_func,
                            on_generation=on_generation,
                            suppress_warnings=True,
                            mutation_percent_genes=10,
                            keep_parents=1,
                            stop_criteria=["reach_10000"],
                            mutation_type='random'
                            )
    
    ga_instance.run()

    print("Train Finished")

    solution, solution_fitness = ga_instance.get_top()

    print(f"Fitness value of the best solution = {solution_fitness}")
    id_s = int(random.random()*1000)
    torch.save(solution,f=f'solution{id_s}')


def eval(s_name):
    solution = torch.load(s_name)

    score = playGame([solution])[0]
    
    print(f"Resultados = {score}")



import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Wrong parameters")
        exit()

    if sys.argv[1] == 'train':
        TRAIN_MODE = 1
        print("Train Starting ... ")
        if len(sys.argv) == 3:
            train(sys.argv[2])
        else:
            train()

    elif sys.argv[1] == 'eval':
        print("Starting eval")
        if len(sys.argv) != 3:
            print("Missing name of solution file")
        eval(sys.argv[2])
    else:
        print(f"Wrong argv {sys.argv[1]}")

    
    

