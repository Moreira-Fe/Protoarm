from pyfirmata import Arduino, SERVO  # Importa a biblioteca pyFirmata para comunicação com a placa Arduino e a constante SERVO
import time  # Importa a biblioteca time para controle de tempo (delays)

board = Arduino('COM3')  # Inicializa a comunicação com a placa Arduino conectada na porta 'COM3'

# Definição dos pinos que controlam os servos
pin1 = 10  # pino para o servo do polegar
pin2 = 9   # pino para o servo do dedo indicador
pin3 = 8   # pino para o servo do dedo médio
pin4 = 7   # pino para o servo do dedo anelar
pin5 = 6   # pino para o servo do dedo mínimo
pin6 = 5   # pino para o servo do pulso

# Configura os pinos definidos como SERVO, permitindo o controle dos motores servos
board.digital[pin1].mode = SERVO  # Configura o pino 10 para controlar um servo motor (polegar)
board.digital[pin2].mode = SERVO  # Configura o pino 9 para controlar um servo motor (indicador)
board.digital[pin3].mode = SERVO  # Configura o pino 8 para controlar um servo motor (médio)
board.digital[pin4].mode = SERVO  # Configura o pino 7 para controlar um servo motor (anelar)
board.digital[pin5].mode = SERVO  # Configura o pino 6 para controlar um servo motor (mínimo)
board.digital[pin6].mode = SERVO  # Configura o pino 5 para controlar um servo motor (pulso)

# Função para girar o servo até um determinado ângulo
def rotateServo(pino, angle):
    board.digital[pino].write(angle)  # Envia o comando para girar o servo até o ângulo especificado
    time.sleep(0.015)  # Espera 15 milissegundos para garantir que o servo complete o movimento

# Função para abrir ou fechar os dedos/pulso
def abrir_fechar(pin, on_off):
    if on_off == 1:  # Se on_off for 1, abre o dedo (ângulo 0)
        rotateServo(pin, 0)
    elif on_off == 0 and pin not in [10, 9, 5]:  # Se on_off for 0 e o pino não for o do polegar, indicador ou pulso, fecha o dedo em 140 graus
        rotateServo(pin, 140)
    elif on_off == 0 and pin == 10:  # Se on_off for 0 e o pino for o do polegar, fecha o polegar em 150 graus
        rotateServo(pin, 150)
    elif on_off == 0 and pin == 9:  # Se on_off for 0 e o pino for o do indicador, fecha o indicador em 180 graus
        rotateServo(pin, 180)
    elif on_off == 0 and pin == 5:  # Se on_off for 0 e o pino for o do pulso, ajusta o pulso em 90 graus
        rotateServo(pin, 90)

# Função para testar todos os servos, movendo-os através de seus ângulos
def testeTodos():
    rotateServo(pin1, 0)  # Move o servo do polegar para o ângulo 0
    rotateServo(pin2, 0)  # Move o servo do indicador para o ângulo 0
    rotateServo(pin3, 0)  # Move o servo do médio para o ângulo 0
    rotateServo(pin4, 0)  # Move o servo do anelar para o ângulo 0
    rotateServo(pin5, 0)  # Move o servo do mínimo para o ângulo 0
    rotateServo(pin6, 0)  # Move o servo do pulso para o ângulo 0
    time.sleep(1)  # Aguarda 1 segundo

    rotateServo(pin1, 150)  # Move o servo do polegar para o ângulo 150
    time.sleep(1)  # Aguarda 1 segundo
    rotateServo(pin1, 0)  # Retorna o servo do polegar para o ângulo 0
    time.sleep(1)  # Aguarda 1 segundo

    rotateServo(pin2, 130)  # Move o servo do indicador para o ângulo 130
    time.sleep(1)  # Aguarda 1 segundo
    rotateServo(pin2, 0)  # Retorna o servo do indicador para o ângulo 0
    time.sleep(1)  # Aguarda 1 segundo

    rotateServo(pin3, 130)  # Move o servo do médio para o ângulo 130
    time.sleep(1)  # Aguarda 1 segundo
    rotateServo(pin3, 0)  # Retorna o servo do médio para o ângulo 0
    time.sleep(1)  # Aguarda 1 segundo

    rotateServo(pin4, 130)  # Move o servo do anelar para o ângulo 130
    time.sleep(1)  # Aguarda 1 segundo
    rotateServo(pin4, 0)  # Retorna o servo do anelar para o ângulo 0
    time.sleep(1)  # Aguarda 1 segundo

    rotateServo(pin5, 130)  # Move o servo do mínimo para o ângulo 130
    time.sleep(1)  # Aguarda 1 segundo
    rotateServo(pin5, 0)  # Retorna o servo do mínimo para o ângulo 0
    time.sleep(2)  # Aguarda 2 segundos

    rotateServo(pin6, 90)  # Move o servo do pulso para o ângulo 90
    time.sleep(1)  # Aguarda 1 segundo
    rotateServo(pin6, 0)  # Retorna o servo do pulso para o ângulo 0
    time.sleep(1)  # Aguarda 1 segundo