"""

A principal razão para a criação desse módulo é para obtermos os valores das posições dos landmarks de forma mais fácil para serem implementados em projetos futuros.

O framework utilizado nesse módulo é o Mediapipe, desenvolvido pelo Google.
o framework permite resolver vários problemas como: detecção de rosto, pontos de referência facial, reconhecimento facial, detecção de objetos, rastreamento de mão
Aqui será utilizado o HandTracking, que utiliza dois módulos principais no back end: Palm Detection e Hand Landmarks
Palm Detection funciona em completar a imagem e fornece uma imagem cortada da mão.
Assim, o Hand Landmark consegue encontrar 21 pontos a partir dessa imagem obtida.
Para treinar a marca da mão, o Google  capturou 30.000 imagens de diferentes mãos. Esse é um dos motivos por ser um framework que funciona tão bem e de forma simples, sem fazer muitas instalações ou alterar configurações
Os únicos pacotes que precisamos instalar é o opencv e o mediapipe

Esse módulo será importado no arquivo ControleLed

Autor:
Bruno Mingoti

Agradecimentos:
O código foi desenvolvido com base em vídeo-aulas desenvolvidas pelo canal no YouTube
Murtaza's Workshop - Robotics and AI
Links:
https://youtu.be/9iEPzbG-xLE
https://youtu.be/p5Z_GGRCI5s

"""


import cv2
import mediapipe as mp
import time


class handDetector(): # inicialização de todos os parâmetros na classe
    def __init__(self, mode=False, maxHands=1, detectionConfidence=0.5, trackingConfidence=0.5): # irei utilizar os mesmos parâmetros que estão disponíveis no arquivos hands.
        # Método definidos dentro dessa classe, fazendo uso uso de um modelo de framework chamado mediapipe já desenvolvido pelo Google
        self.mode = mode
        self.maxHands = maxHands
        self.detectionConfidence = detectionConfidence
        self.trackingConfidence = trackingConfidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionConfidence, self.trackingConfidence) # (*)
        self.mpDesenho = mp.solutions.drawing_utils


    def findHands(self, img, desenho=True): # precisamos de uma imagem para encontrar as mãos
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.resultados = self.hands.process(imgRGB)
        if self.resultados.multi_hand_landmarks:
            for handLandMarks in self.resultados.multi_hand_landmarks:
                if desenho:# vou checar se quero que as landmarks sejam desenhadas ou não
                    self.mpDesenho.draw_landmarks(img, handLandMarks, self.mpHands.HAND_CONNECTIONS)
        return img # agora devo retornar a imagem com os resultados processados neste método


    def findPosition(self, img, handNumber=0, desenho=False):
        landmarkList = [] # é a lista com os valores de todas as posições dos pontos que irei retornar
        # irei checar de novo se os landmarks ou mãos foram detectados ou não. Se self.resultados dos landmarks de múltiplas mãos estão disponíveis, então vamos checar as próximas linhas
        if self.resultados.multi_hand_landmarks:
            # agora preciso especificar  qual mão estou falando, pois antes em findHands eu estava tratando de todas elas
            myHand = self.resultados.multi_hand_landmarks[handNumber] # irei especificar qual mão
            for id, lm in enumerate(myHand.landmark): # e a partir dessa mão, o programa irá obter e colocar os landmarks dentro de uma lista
                    a, l, c = img.shape
                    cx, cy = int(lm.x * l), int(lm.y * a)
                    landmarkList.append([id, cx, cy])
                    if desenho:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
        return landmarkList # independentemente de estar vazio ou não irei retornar as listas com os valores


def main():
    tempoAtual = 0
    tempoAnterior = 0
    camera = cv2.VideoCapture(0)
    detector = handDetector() # não irei passar nenhum parâmetro, pois sei que o método já possui parâmetros opcionais
    while True: #depois que todas as variáveis e objetos da classe foram declarados
        success, img = camera.read() # vou capturar a imagem
        img = detector.findHands(img) # vou enviar essa imagem para o método findHands
        landmarkList = detector.findPosition(img)
        print(landmarkList)

        tempoAtual = time.time()
        fps = 1 / (tempoAtual - tempoAnterior)
        tempoAnterior = tempoAtual

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow('Image', img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
