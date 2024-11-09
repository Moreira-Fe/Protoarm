#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <PID_v1.h>
#include <Adafruit_VL53L0X.h>  // Biblioteca para o sensor de proximidade VL53L0X

// Instância para o driver PWM do PCA9685
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
Adafruit_VL53L0X lox = Adafruit_VL53L0X();  // Instância do sensor de proximidade VL53L0X

// Configura os pinos dos botões
const int fecharDedosButtonPin = 12;  // Botão para fechar os dedos
const int abrirDedosButtonPin = 14;   // Botão para abrir os dedos

// Pinos e canais do potenciômetro e do sensor ACS712
const int potPin = 34;        // Potenciômetro para ajustar a velocidade dos servos
const int ACS712Pin = 35;     // Pino de leitura do sensor ACS712 de corrente

// Definindo os canais dos servos no PCA9685
const int POLEGAR = 0;
const int INDICADOR = 1;
const int MEDIO = 2;
const int ANELAR = 3;
const int MINIMO = 4;
const int PULSO = 5;

// Definições de PWM para os ângulos dos servos
#define SERVOMIN 150          // PWM mínimo correspondente a 0 graus
#define SERVOMAX 600          // PWM máximo correspondente a 130 graus
#define PULSOMAX 400          // PWM máximo para o pulso a 60 graus

// Variáveis para o controle PID (Feedback de corrente)
double setpoint, input, output;
double Kp = 2.0, Ki = 5.0, Kd = 2.0;
PID myPID(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);

// Variáveis para leitura de distância e corrente
int distancia;                // Distância medida pelo sensor VL53L0X
double corrente;              // Corrente medida pelo sensor ACS712
bool dedosFechados = false;   // Flag para saber se os dedos estão fechados
bool aguardandoFechar = false; // Flag para aguardar o fechamento dos dedos

void setup() {
  // Inicia a comunicação serial
  Serial.begin(115200);
  
  // Inicializa o driver PWM e define a frequência para os servos
  pwm.begin();
  pwm.setPWMFreq(60);

  // Configura os pinos dos botões como entradas com pull-up interno
  pinMode(fecharDedosButtonPin, INPUT_PULLUP);
  pinMode(abrirDedosButtonPin, INPUT_PULLUP);

  // Inicializa os servos em 0 graus
  moverServo(POLEGAR, 0, 0);
  moverServo(INDICADOR, 0, 0);
  moverServo(MEDIO, 0, 0);
  moverServo(ANELAR, 0, 0);
  moverServo(MINIMO, 0, 0);
  moverServo(PULSO, 0, 0);

  // Inicializa o sensor de proximidade VL53L0X
  if (!lox.begin()) {
    Serial.println("Erro ao iniciar o sensor VL53L0X!");
    while (1);
  }

  // Configura o PID e seus limites de saída
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(5, 50);  // Define limites de atraso em milissegundos
}

void loop() {
  // Lê o estado dos botões
  int fecharDedosState = digitalRead(fecharDedosButtonPin);
  int abrirDedosState = digitalRead(abrirDedosButtonPin);

  // Lê o valor do potenciômetro e mapeia para um intervalo de tempo de atraso
  int potValue = analogRead(potPin);
  int delayTime = map(potValue, 0, 4095, 5, 50); // Ajusta o tempo de atraso conforme o potenciômetro

  // Atualiza o valor de entrada do PID com a corrente lida pelo ACS712
  corrente = lerCorrente();
  input = corrente;  // Define a corrente como entrada do PID
  myPID.Compute();   // Calcula a saída do PID

  // Leitura da distância com o sensor VL53L0X
  VL53L0X_RangingMeasurementData_t measure;
  lox.rangingTest(&measure, false);

  // Atualiza a variável `distancia` se a leitura for válida
  if (measure.RangeStatus != 4) {
    distancia = measure.RangeMilliMeter;
  } else {
    distancia = -1; // Indica erro de leitura
  }

  // Condição de fechamento manual dos dedos, mas aguarda o sensor de proximidade
  if (fecharDedosState == LOW && !dedosFechados) {
    aguardandoFechar = true;  // Inicia o processo de fechamento dos dedos
    Serial.println("Aguardando objeto a 4 mm para fechar os dedos...");
  }

  // Verifica a proximidade do objeto para fechar os dedos
  if (aguardandoFechar && distancia > 0 && distancia <= 28) {
    moverDedos(130, output);  // Fecha os dedos a 130 graus
    dedosFechados = true;
    aguardandoFechar = false;
    Serial.println("Dedos fechados.");
  }

  // Condição de abertura dos dedos quando o botão "abrir dedos" for pressionado
  if (abrirDedosState == LOW && dedosFechados) {
    moverDedos(0, output);    // Abre os dedos a 0 graus
    dedosFechados = false;
    Serial.println("Dedos abertos.");
  }

  // Exibe os valores de distância e corrente no terminal serial
  Serial.print("Distância: ");
  Serial.print(distancia);
  Serial.print(" mm | Corrente: ");
  Serial.print(corrente, 3);
  Serial.print(" A | PID Output: ");
  Serial.println(output);

  delay(100); // Atraso para evitar leituras erradas
}

// Função para ler a corrente do ACS712
double lerCorrente() {
  int adcValue = analogRead(ACS712Pin);
  double voltage = (adcValue / 4095.0) * 3.3; // Converte a leitura para tensão (ESP32 usa 3.3V)
  double corrente = (voltage - 2.5) / 0.066;  // Calcula corrente baseado na sensibilidade do ACS712
  return corrente;
}

// Função para mover um servo para um ângulo específico com atraso
void moverServo(int canal, int angulo, int delayTime) {
  int pwmValue = (canal == PULSO) ? map(angulo, 0, 60, SERVOMIN, PULSOMAX) : servoAngleToPWM(angulo);
  pwm.setPWM(canal, 0, pwmValue);
  Serial.print("Movendo Servo ");
  Serial.print(canal);
  Serial.print(" para ângulo ");
  Serial.println(angulo);
  delay(delayTime);
}

// Função para mover todos os dedos ao mesmo tempo
void moverDedos(int angulo, int delayTime) {
  moverServo(POLEGAR, angulo, delayTime);
  moverServo(INDICADOR, angulo, delayTime);
  moverServo(MEDIO, angulo, delayTime);
  moverServo(ANELAR, angulo, delayTime);
  moverServo(MINIMO, angulo, delayTime);
}

// Função para converter ângulo para valor de PWM
int servoAngleToPWM(int angle) {
  return map(angle, 0, 130, SERVOMIN, SERVOMAX);
}
