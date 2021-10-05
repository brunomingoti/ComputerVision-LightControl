#                                          Sistema de Controle de Luminosidade por Visão Computacional 👀:



> Status do Projeto: :heavy_check_mark: (pronto)

### Tópicos :writing_hand:

- [Descrição do projeto](#descrição-do-projeto-file_folder)

- [Deploy da Aplicação](#deploy-da-aplicação-dash)

- [Pré-requisitos](#pré-requisitos-pushpin)

- [Como rodar a aplicação](#como-rodar-a-aplicação-arrow_forward)
- [Observações](#observações-eyes)
- [Bibliotecas utilizadas](#bibliotecas-utilizadas-books) 
- [Possíveis melhorias](#melhorias-rocket)
- [Desenvolvedores e Contribuintes](#desenvolvedores-e-contribuintes-computer)
- [Licença](#licença-grey_exclamation)



## Descrição do projeto :file_folder:

<p align="justify">
  Controlar qual/quais LEDs ligar e a sua luminosidade por meio do processamento de imagem dos gestos das mãos utilizando o conceito de Visão Computacional.
  Foi utilizado o Python como código principal e que depois foi integrado com um Arduino UNO que controlará um circuito simples de LEDs que estão em uma protoboard.
</p>



## Deploy da Aplicação :dash:

EM CONSTRUÇÃO



## Pré-requisitos :pushpin:
Material:

```
Arduino UNO
```

```
Protoboard
```

```
5 LEDs
```

```
5 resistores (nesse caso foi utilizado 1k omh.
O ideal seria a utilização de uma resistência menor para não prejudicar na luminosidade,
mas mudanças no código podem ser necessárias na parte do intervalo do tamanho da linha que
liga a ponta do indicador e a ponta do polegar).
```

```
11 jumpers macho/macho
```

No Python:

```
pip install mediapipe
```

```
pip install numpy
```

```
pip install opencv-python
```

```
pip install pyserial
```


## Como rodar a aplicação :arrow_forward:

- Monte o circuito em uma protoboard.
- Conecte ao Arduino UNO e ligue ao computador.
- Carregue o código C++ no Arduino.
- Certifique-se de que a câmera e a porta selecionadas no código Python são as corretas.
- O controle da luminosidade deve ser adaptada de acordo com a câmera utilizada.Adaptações podem ser necessárias. Coloque comandos de print em locais estratégicos para facilitar a análise.



## Observações :eyes:

O projeto parte da premissa do conceito de Visão Computacional, realizando o processamento de imagem dos gestos das mãos obtida através da webcam e interpretada por meio do módulo HandTrackingModule, módulo que utiliza o framework mediapipe, propriedade da Google, para a identificação da mão.
A partir disso, conseguimos controlar LEDs que estão conectados a um Arduino UNO que, por sua vez, está conectado ao computador pela porta USB.

O programa irá levar em consideração qual mão está sendo utilizada, sendo que:
- MÃO DIREITA: Controla qual/quais LEDS acender. Cada dedo corresponde a um LED específico.
- MÃO ESQUERDA: Controla a luminosidade dos LEDs que escolhi acender anteriormente pela mão direita.

O código só será executado corretamente se houver um Arduino conectado na porta Serial indicada na linha 50.
Certifique-se em qual porta está conectada em seu computador e adapte caso seja necessário.
Além disso, lembre-se de selecionar a câmera correta na linha 42, normalmente será o valor 0.

O controle da luminosidade deve ser adaptada de acordo com a câmera utilizada. Adaptações podem ser necessárias.
Coloque comandos de print em locais estratégicos para facilitar a análise.

APROVEITE!



## Bibliotecas utilizadas :books:

- [MediaPipe]
- [NumPy]
- [PySerial]
- [Math]
- [Time]



## Possíveis melhorias :rocket:

:memo: Adaptar o código para reconhecer as duas mãos simultaneamente;



## Desenvolvedores e Contribuintes :computer:

- Bruno Mingoti - [LinkedIn]( https://www.linkedin.com/in/brunomingoti/) - [Email](brunomingoti@gmail.com)

Agradecimentos:
- O código foi desenvolvido com base em vídeo-aulas desenvolvidas pelo canal no YouTube Murtaza's Workshop - Robotics and AI
Links:
https://youtu.be/9iEPzbG-xLE
https://youtu.be/p5Z_GGRCI5s



## Licença :grey_exclamation:

The [MIT License]() (MIT)
