// O código será executado com base nos dados que estão sendo gerados e enviados pelo Python via porta serial.

#define led1 3
#define led2 5
#define led3 6
#define led4 9
#define led5 10

int incomingByte = 0; // para dados recebidos na porta Serial --> As informações geradas pelo Python passarão por essa variável
int valor;
int ligado1 = 0;
int ligado2 = 0;
int ligado3 = 0;
int ligado4 = 0;
int ligado5 = 0;

void setup() {
  Serial.begin(9600); //Inicializei a porta serial com a taxa de transmissão padrão de 9600 bps
  //Inicializei pinos pwm (para conseguir realizar o efeito de controle de luminosidade) como saída para cada LED
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);
  
  
}
void loop() {
  
  char serialInfo[5];
  //Serial.available retorna o número de bytes (caracteres) disponíveis para leitura da porta serial
  // Enviar resposta apenas quando receber dados:
  if (Serial.available() > 0) {
    //Lê caracteres da porta serial e os move para um buffer. A função termina se a quantidade de bytes determinada foi lida.
    //Retorna o NÚMERO de caracteres colocados no buffer, no qual 0 indica que os dados não foram encontrados
    // Parâmetros: 
    // Buffer (o buffer para se armazenar os bytes, podendo ser char[] ou byte[]) e length (número de bytes a serem lidos, devendo ser int)
    
    incomingByte = Serial.readBytes(serialInfo, 5); // Exemplo: serialInfo --> ['1','0','2']. Retorna 3 que foi a quantidade de caracteres colocados no buffer

    // Quando rodamos Serial.read() ou Serial.readBytes() há um retorno de um dígito.
    // Exemplo: Se o valor lido for 560, o primeiro Serial.read() irá retornar apenas 5, o segundo 6 e o terceiro 0

    //Abaixo irei converter o valor em char em cada uma das posições e converter para int:

    // Tenho que fazer uma estrutura de condição aqui para determinar qual é o valor
    //se é o tamanho (valor entre 2000 e 20330, lembrando que esses números podem varia dependendo da webcam) ou a quantidade de dedos (entre 00000 e 11111, onde 0 indica nenhum dedo levantado e 11111 todos os dedos levantados)
    
    int d1 = serialInfo[0]-'0';
    int d2 = serialInfo[1]-'0';
    int d3 = serialInfo[2]-'0';
    int d4 = serialInfo[3]-'0';
    int d5 = serialInfo[4]-'0';
    
    
    int valor = d1*10000 + d2*1000 + d3*100 + d4*10 + d5; //transformando os dígitos em um valor numérico único
    
    if(valor >= 0) {
      if (valor >= 00000 && valor <= 11111) {
        if (d1 == 1) {
          digitalWrite(led1, HIGH);
          ligado1 = 1;
        } else {
          digitalWrite(led1, LOW);
          ligado1 = 0;
        }
        if (d2 == 1) {
          digitalWrite(led2, HIGH);
          ligado2 = 1;
        } else {
          digitalWrite(led2, LOW);
          ligado2 = 0;
        }
        if (d3 == 1) {
          digitalWrite(led3, HIGH);
          ligado3 = 1;
        } else {
          digitalWrite(led3, LOW);
          ligado3 = 0;
        }
        if (d4 == 1) {
          digitalWrite(led4, HIGH);
          ligado4 = 1;
        } else {
          digitalWrite(led4, LOW);
          ligado4 = 0;
        }
        if (d5 == 1) {
          digitalWrite(led5, HIGH);
          ligado5 = 1;
        } else {
          digitalWrite(led5, LOW);
          ligado5 = 0;
        }
      } else {
        //Com esse valor faço um mapeamento. Uma conversão para os valores 0 e 255 que correponde aos 8 bits(0 é o valor mínimo e 255 é o valor máximo) de saída da porta de saída número 11 que irão proporcionalmente corresponder entre um fator de 0 a 5V de saída também no pino 11. Basicamente a função faz uma regra de 3.
        valor = map(valor, 20000, 20330, 0, 255);

        if (ligado1 == 1) {
         analogWrite(led1, valor); // e faz uma escrita analógica na porta número ligado{num]
        }
        if (ligado2 == 1) {
         analogWrite(led2, valor);
        }
        if (ligado3 == 1) {
         analogWrite(led3, valor);
        }
        if (ligado4 == 1) {
         analogWrite(led4, valor);
        }
        if (ligado5 == 1) {
         analogWrite(led5, valor);
        }
        delay(1);
      }
    }
  }
}
