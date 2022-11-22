class StudentClassifier():
    def __init__(self):
        pass

    # Quais são os tipos dos objetos
    # 0 -> Bird
    # 1 -> Small Cactus
    # 2 -> Large Cactus
    # Outputs:
    # - "K_DOWN" : O dino abaixo
    # - "K_UP" : O dino pula
    # - "K_NO" : O dino não faz nada
    def keySelector(self, distancia_do_obstaculo : int, altura_do_obstaculo : int, velocidade_do_dino : int, tipo_do_objeto : int):
        if (300 > distancia_do_obstaculo > 0 and not (tipo_do_objeto == 0)):
            return "K_UP"
        elif (tipo_do_objeto == 0 and distancia_do_obstaculo < 300):
            return "K_DOWN"
        else:
            return "K_NO"
