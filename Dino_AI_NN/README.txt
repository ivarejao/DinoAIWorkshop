# Inteligência Artificial para Chrome Dinossaur

Implementação de Inteligência Artificial para o jogo do Dinossauro do Chrome usando Algoritmo Genético com Redes Neurais

## Passos

### Instalações

Essa implementação foi feita utilizando Python3.8.3, você pode baixá-lo [aqui](https://www.python.org/downloads/).
Para rodá-la é necessário instalar algumas dependencias, para isso, rode o comando abaixo no terminal:
```
pip3 install -r requirements.txt
```

### Rodar a implementação
##### Treinamento
Para treinar o dino execute no terminal:

```bash
python3 main.py train
```

##### Melhor Dino
Para rodar o DinoGame com a melhor rede treinada execute no terminal o seguinte comando

```bash
python3 main.py eval best_solution
```