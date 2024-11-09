import cv2  # Importa a biblioteca OpenCV para processamento de imagens
import mediapipe as mp  # Importa a biblioteca MediaPipe para detecção e rastreamento de mãos
import servo as mao  # Importa o módulo personalizado para controle dos servos motores

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Inicializa a captura de vídeo da webcam
cap.set(3, 640)  # Define a largura do vídeo para 640 pixels
cap.set(4, 480)  # Define a altura do vídeo para 480 pixels

hands = mp.solutions.hands  # Carrega o módulo de mãos do MediaPipe
Hands = hands.Hands(max_num_hands=1)  # Cria um objeto para detectar no máximo uma mão
mpDraw = mp.solutions.drawing_utils  # Utilitário para desenhar as landmarks das mãos na imagem

while True:  # Loop principal
    success, img = cap.read()  # Captura uma imagem da webcam
    frameRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte a imagem para RGB
    results = Hands.process(frameRGB)  # Processa a imagem para detectar landmarks das mãos
    handPoints = results.multi_hand_landmarks  # Obtém os pontos das landmarks da mão detectada
    h, w, _ = img.shape  # Obtém a altura e largura da imagem
    pontos = []  # Inicializa uma lista para armazenar os pontos das landmarks

    if handPoints:  # Se landmarks de mão forem detectados
        for points in handPoints:  # Para cada conjunto de pontos das landmarks detectadas
            mpDraw.draw_landmarks(img, points, hands.HAND_CONNECTIONS)  # Desenha as landmarks e conexões das mãos na imagem
            for id, cord in enumerate(points.landmark):  # Enumera os pontos das landmarks
                cx, cy = int(cord.x * w), int(cord.y * h)  # Converte as coordenadas normalizadas para pixels
                cv2.circle(img, (cx, cy), 4, (255, 0, 0), -1)  # Desenha um círculo nos pontos das landmarks
                pontos.append((cx, cy))  # Armazena as coordenadas dos pontos na lista `pontos`

        if pontos:  # Se `pontos` não estiver vazia
            distPolegar = abs(pontos[17][0] - pontos[4][0])  # Calcula a distância horizontal entre a base e a ponta do polegar
            distIndicador = pontos[5][1] - pontos[8][1]  # Calcula a distância vertical entre a base e a ponta do dedo indicador
            distMedio = pontos[9][1] - pontos[12][1]  # Calcula a distância vertical entre a base e a ponta do dedo médio
            distAnelar = pontos[13][1] - pontos[16][1]  # Calcula a distância vertical entre a base e a ponta do dedo anelar
            distMinimo = pontos[17][1] - pontos[20][1]  # Calcula a distância vertical entre a base e a ponta do dedo mínimo

            if distPolegar < 80:  # Se a distância entre a base e a ponta do polegar for menor que 80 pixels
                mao.abrir_fechar(10, 0)  # Fecha o servo do polegar (posição 0)
            else:  # Caso contrário
                mao.abrir_fechar(10, 1)  # Abre o servo do polegar (posição 1)

            if distIndicador >= 1:  # Se a distância entre a base e a ponta do dedo indicador for maior ou igual a 1 pixel
                mao.abrir_fechar(9, 1)  # Abre o servo do dedo indicador (posição 1)
            else:  # Caso contrário
                mao.abrir_fechar(9, 0)  # Fecha o servo do dedo indicador (posição 0)

            if distMedio >= 1:  # Se a distância entre a base e a ponta do dedo médio for maior ou igual a 1 pixel
                mao.abrir_fechar(8, 1)  # Abre o servo do dedo médio (posição 1)
            else:  # Caso contrário
                mao.abrir_fechar(8, 0)  # Fecha o servo do dedo médio (posição 0)

            if distAnelar >= 1:  # Se a distância entre a base e a ponta do dedo anelar for maior ou igual a 1 pixel
                mao.abrir_fechar(7, 1)  # Abre o servo do dedo anelar (posição 1)
            else:  # Caso contrário
                mao.abrir_fechar(7, 0)  # Fecha o servo do dedo anelar (posição 0)

            if distMinimo >= 1:  # Se a distância entre a base e a ponta do dedo mínimo for maior ou igual a 1 pixel
                mao.abrir_fechar(6, 1)  # Abre o servo do dedo mínimo (posição 1)
            else:  # Caso contrário
                mao.abrir_fechar(6, 0)  # Fecha o servo do dedo mínimo (posição 0)

            # Verificação se todos os dedos estão fechados
            if all([
                distPolegar < 80, 
                distIndicador < 1, 
                distMedio < 1, 
                distAnelar < 1, 
                distMinimo < 1
            ]):
                # Se todos os dedos estão fechados, detecta movimento rotacional
                distRotacao = pontos[0][0] - pontos[9][0]  # Calcula a diferença na posição X entre o pulso e o ponto central do indicador
                
                if distRotacao > 10:  # Se houver rotação à direita (arbitrariamente definido como > 10 pixels)
                    mao.abrir_fechar(5, 1)  # Gira o servo do pulso em uma direção
                elif distRotacao < -10:  # Se houver rotação à esquerda (arbitrariamente definido como < -10 pixels)
                    mao.abrir_fechar(5, 0)  # Gira o servo do pulso na direção oposta

    cv2.imshow('Imagem', img)  # Mostra a imagem em uma janela chamada "Imagem"
    cv2.waitKey(1)  # Aguarda 1 milissegundo por uma tecla pressionada, permitindo atualizar a janela da imagem