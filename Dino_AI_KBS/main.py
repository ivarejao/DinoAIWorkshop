from play import *
from RuleBasedClassifier import *
import constants



if __name__ == '__main__':
    constants.AI_MODE = 'RB'
    
    print('Rule Based Classifier professor')
    constants.aiPlayer = RuleBasedKeyClassifier()

    score = playGame()
    print(score)