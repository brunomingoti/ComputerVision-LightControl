"""

Projeto de SISTEMA DE CONTROLE DE LUMINOSIDADE POR VISÃO COMPUTACIONAL

O projeto parte da premissa do conceito de Visão Computacional, realizando o processamento de imagem dos gestos das mãos
obtida através da webcam e interpretada por meio do módulo HandTrackingModule, módulo que
utiliza o framework mediapipe, propriedade da Google, para a identificação da mão.

O programa irá levar em consideração qual mão está sendo utilizada, sendo que:
- MÃO DIREITA: Controla qual/quais LEDS acender. Cada dedo corresponde a um LED específico.
- MÃO ESQUERDA: Controla a luminosidade dos LEDs que escolhi acender anteriormente pela mão direita.
Possível melhoria: Adaptar o código para reconhecer as duas mãos simultaneamente.

O código só será executado corretamente se houver um Arduino conectado na porta Serial indicada na linha 50.
Certifique-se em qual porta está conectada em seu computador e adapte caso seja necessário.
Além disso, lembre-se de selecionar a câmera correta na linha 42, normalmente será o valor 0.

O controle da luminosidade deve ser adaptada de acordo com a câmera utilizada. Adaptações podem ser necessárias.
Coloque comandos de print em locais estratégicos para facilitar a análise.

APROVEITE!

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
import time
import numpy as np
import HandTrackingModule as htm # Classe referente a detecção e criação das landmarks na mão
import math


# Importação para a integração com o Arduino
import serial

larguraCamera, alturaCamera = 640, 480

# Configurações iniciais da webcam para fazer a captura
camera = cv2.VideoCapture(1) # Caso dê algum problema na câmera alterar aqui o valor para zero - Alternância entre as câmeras
camera.set(3, larguraCamera)
camera.set(4, alturaCamera)
tempoAnterior = 0

# vou criar um objeto dessa classe chamada detector
detector = htm.handDetector(detectionConfidence=0.8) #parâmetros já estão como opcionais no módulo. Alterei a confiança da detecção (ter certeza que tem uma mão). Assim, quando estiver alterando o volume, o movimento será mais suave sem que a imagem falhe. Reconhece a mão com uma maior precisão.

# Comandos da Porta Serial
portaSerial = serial.Serial.close
portaSerial = serial.Serial('COM5', 9600) # quando conecto uma placa Arduino no computador, ocorre a montagem dessa placa em uma determinada porta usb/porta COM (comunicação Serial), que irá aparecer na aba ferramentas da IDE do Arduino. 9600 indica a taxa de treansmissão padrão
portaSerial.timeout = 1

volBarra = 400
volPorcentagem = 0
tipIds = [4, 8, 12, 16, 20]
tamanho = 0
totalFingers = 0

while True:
    success, img = camera.read() # captura da imagem
    img = detector.findHands(img) # vou encontrar a mão utilizando o método findhand do HandTrackingModule

    # Irei obter as posições do dedos para controlar a luminosidade:
    landmarkList = detector.findPosition(img)

    if len(landmarkList) != 0:
        if landmarkList[4][1] < landmarkList[17][1]:
            # eu apenas estou interessado em pegar as informações dos pontos 4 (polegar) e 8 (indicador)
            # vou criar círculos em volta desses dois pontos no indicador e polegar:
            cx4, cy4 = landmarkList[4][1], landmarkList[4][2] # vou indicar o ponto do centro do local onde quero fazer o círculo, informando qual dedo e qual índice da lista que estou falando
            cx8, cy8 = landmarkList[8][1], landmarkList[8][2]

            cxlinha, cylinha = (cx4 + cx8) // 2, (cy8 + cy4) // 2 #Preciso encontrar o centro dessa linha, realizando uma divisão inteira com //, para tomar como ponto de referência na hora de alterar a luminosidade:

            cv2.circle(img, (cx4, cy4), 15, (255, 0, 0), cv2.FILLED) # o 15 indica o raio do círculo, depois cor
            cv2.circle(img, (cx8, cy8), 15, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (cx4, cy4), (cx8, cy8), (255, 0, 0), 3) # Estou desenhando uma linha entre esses dois pontos informados como parâmetros
            cv2.circle(img, (cxlinha, cylinha), 15, (255, 0, 0), cv2.FILLED)

            #Preciso descobrir qual é o tamanho da linha criada entre os pontos 4 e 8, assim consigo alterar a luminosidade baseado nisso
            tamanho = math.hypot(cx8 - cx4, cy8 - cy4) # utilizei a biblioteca math
            # Hand Range é 40 a 240
            # Volume Range é -65 a 0
            # Preciso converter os valores Hand Range para o Volume Range:
            # Com base no valor obtido do tamanho irei realizar o mapeamento lá no código do Arduino

            tamanhoArduino = str(int(20000 + tamanho))
            print(tamanhoArduino)

            # Agora irei enviar a variável tamanhoArduino para o Arduino através da porta Serial:
            portaSerial.write(tamanhoArduino.encode()) #tenho que passar utilizando esse método para enviar o conteúdo da variável, se não ela seria entendida como uma String qualquer.
            # Caso eu não estivesse tratando de variáveis, teria que usar uma sintaxe para enviar o valor em binário. Não poderia usar (b'tamanhoArduino'), pois estaria passando a palavra tamanhoArduino e não o conteúdo dessa variável propriamente dita.

            volBarra = np.interp(tamanho, [40, 240], [400, 150])
            volPorcentagem = np.interp(tamanho, [40, 240], [0, 100]) # ANALISAR ESSES NÚMEROS

            if tamanho < 40: # se for menor que 40 vou alterar a cor do círculo
                cv2.circle(img, (cxlinha, cylinha), 15, (0, 255, 0), cv2.FILLED) # vai dar um efeito de botão

            # Irei mostrar um retângulo com o número do volume para ficar algo mais visual
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3) # estou passando como parâmetro a posição que quero que apareça o retângulo: posição inicial e final, cor e largura da linha (no lugar de cv2.FILLED). Nesse caso, o tamanho do retângulo ficará 85-50=35
            cv2.rectangle(img, (50, int(volBarra)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPorcentagem)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        if landmarkList[4][1] > landmarkList[17][1]:
            # Nessa estrutura que irei determinar os cenários dos dedos
            # Queremos pegar a ponta dos dedos e baseado no valor desses pontos decidir se a mão está fechada ou não. Para isso iremos pegar os pontos 4, 8, 12, 16, 20
            # É possível encontrar os números de cada ponto no site oficial do mediapipe.
            # vamos verificar se os landmarks das pontas dos dedos estão abaixo de outros pontos. Exemplo: Se 8 está abaixo de 6, então o dedos está fechado
            fingers = [0, 0, 0, 0, 0]  # [polegar, indicador, dedo médio, anelar, dedo mínimo] preciso salvar essa informação para saber se os dedos estão abertos ou fechados

            # Polegar
            if landmarkList[tipIds[0]][1] > landmarkList[tipIds[0] - 1][1]:  # estou pegando o valor de x, por isso índice 1. Se for verdade, quer dizer que a mão está aberta. Estou comparando os pontos 3 e 4 do polegar
                    # para o caso do polegar, posso colocar para caso a ponta do dedo estiver à direita do ponto-1, significa que está aberto, senão, indica estar fechado.
                    # Primeiro, irei verificar qual mão se trata e baseado nisso consigo alterar os parâmetros
                fingers[0] = 1 #indica que o dedo está levantado

            else:
                fingers[0] = 0 # indica que o dedo está fechado

                # Outros dedos - TENHO QUE SEPARAR PARA CADA DEDO
            for id in range(1, 5):  # vou colocar o loop para 4 dedos, já que o polegar não irá funcionar aqui
                if landmarkList[tipIds[id]][2] < landmarkList[tipIds[id] - 2][2]:  # estou pegando o valor de y, por isso índice 2. Se for verdade, quer dizer que a mão está aberta - PROBLEMA: POLEGAR NUNCA FICA ABAIXO DO PONTO DE REFRÊNCIA. Por essa razão esse dedo foi tratado separadamente utilizando o eixo x.
                    if id == 1:
                            fingers[1] = 1
                    if id == 2:
                            fingers[2] = 1
                    if id == 3:
                            fingers[3] = 1
                    if id == 4:
                            fingers[4] = 1
                else:
                    fingers[id] = 0
                    # A partir disso terei uma lista indicando quais dedos estão levantados e quais não estão

            ligados = (''.join(str(fingers).strip('[]').replace(', ', ''))) #Estou "desmembrando" a lista
            print(ligados)
            portaSerial.write(ligados.encode()) #O valor obtido será enviado via porta serial para o Arduino.

    tempoAtual = time.time()
    fps = 1 / (tempoAtual-tempoAnterior)
    tempoAnterior = tempoAtual

    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Img', img)
    cv2.waitKey(10)

portaSerial = serial.Serial.close
