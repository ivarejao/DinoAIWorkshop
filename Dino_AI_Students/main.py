from Students_AI import StudentClassifier
import sys
sys.path.append("./Dino")
from play import playGame
import constants as cons

if __name__ == '__main__':

    cons.AI_MODE = 'RB'

    cons.aiPlayer = StudentClassifier()
    
    score = playGame()

    with open(".resultados", "a") as f:
        f.write(str(score) + "\n")


