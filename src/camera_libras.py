import pygame
import cv2
import numpy as np
import mediapipe as mp
import time
import math

class ReconhecimentoLibras:
    def __init__(self):
        print("✅ Inicializando sistema de reconhecimento de Libras...")
        
        # Inicializar MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Configurar detecção de mãos
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        self.ativa = False
        self.cap = None
        self.frame_atual = None
        self.ultimo_sinal_tempo = 0
        self.sinal_atual = None
        self.contador_frames = 0
        
        # Histórico de gestos para melhor detecção
        self.historico_gestos = []
        self.max_historico = 10
        
        print("✅ Sistema MediaPipe Hands inicializado!")
    
    def iniciar_camera(self):
        """Inicia a câmera real com reconhecimento de mãos"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("❌ Não foi possível abrir a câmera")
                return self._iniciar_camera_simulada()
                
            # Configurar câmera
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.ativa = True
            print("📷 Câmera real com reconhecimento de Libras iniciada!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar câmera: {e}")
            return self._iniciar_camera_simulada()
    
    def _iniciar_camera_simulada(self):
        """Inicia câmera simulada como fallback"""
        print("🔧 Usando câmera simulada com detecção simulada")
        self.ativa = True
        self.cap = None
        self.frame_atual = pygame.Surface((640, 480))
        return True
    
    def _processar_frame_mediapipe(self, frame):
        """Processa frame com MediaPipe para detectar mãos e gestos"""
        # Converter BGR para RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        
        # Detectar mãos
        resultados = self.hands.process(frame_rgb)
        
        # Converter de volta para BGR para desenhar
        frame_rgb.flags.writeable = True
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        gesto_detectado = None
        landmarks = []
        
        if resultados.multi_hand_landmarks:
            for hand_landmarks in resultados.multi_hand_landmarks:
                # Desenhar landmarks das mãos
                self.mp_drawing.draw_landmarks(
                    frame_bgr,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Extrair coordenadas dos landmarks
                landmarks_frame = []
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    h, w, c = frame_bgr.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    landmarks_frame.append((x, y, landmark.z))
                
                landmarks.append(landmarks_frame)
                
                # Reconhecer gesto
                gesto = self._reconhecer_gesto(landmarks_frame)
                if gesto:
                    gesto_detectado = gesto
        
        return frame_bgr, gesto_detectado, landmarks
    
    def _reconhecer_gesto(self, landmarks):
        """Reconhece gestos específicos de Libras baseado na posição dos dedos"""
        if len(landmarks) < 21:
            return None
        
        # Extrair pontos importantes
        punho = landmarks[0]
        polegar_ponta = landmarks[4]
        indicador_ponta = landmarks[8]
        medio_ponta = landmarks[12]
        anelar_ponta = landmarks[16]
        mindinho_ponta = landmarks[20]
        
        indicador_base = landmarks[5]
        medio_base = landmarks[9]
        anelar_base = landmarks[13]
        mindinho_base = landmarks[17]
        
        # Calcular distâncias entre dedos
        def distancia(p1, p2):
            return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        
        # Gesto: POLEGAR PARA CIMA (Ônibus)
        if (polegar_ponta[1] < indicador_base[1] and  # Polegar acima dos outros dedos
            indicador_ponta[1] > indicador_base[1] and  # Outros dedos flexionados
            medio_ponta[1] > medio_base[1] and
            anelar_ponta[1] > anelar_base[1] and
            mindinho_ponta[1] > mindinho_base[1]):
            return "onibus"
        
        # Gesto: MÃO ABERTA (Terminal)
        if (distancia(polegar_ponta, indicador_ponta) > 50 and
            distancia(indicador_ponta, medio_ponta) > 30 and
            distancia(medio_ponta, anelar_ponta) > 30 and
            distancia(anelar_ponta, mindinho_ponta) > 30):
            return "terminal"
        
        # Gesto: INDICADOR PARA CIMA (Qual)
        if (indicador_ponta[1] < indicador_base[1] and  # Indicador estendido
            polegar_ponta[1] < polegar_ponta[1] and     # Polegar não interfere
            medio_ponta[1] > medio_base[1] and          # Outros dedos flexionados
            anelar_ponta[1] > anelar_base[1] and
            mindinho_ponta[1] > mindinho_base[1]):
            return "qual"
        
        # Gesto: APONTAR PARA PULSO (Horas)
        if (indicador_ponta[0] < punho[0] and          # Indicador apontando para pulso
            distancia(indicador_ponta, punho) < 80):    # Perto do pulso
            return "horas"
        
        # Gesto: APONTAR PARA CENTRO (Centro)
        if (indicador_ponta[0] > punho[0] + 50 and     # Indicador apontando para centro
            medio_ponta[1] > medio_base[1]):           # Mão fechada parcialmente
            return "centro"
        
        # Gesto: MÃO PLANANDO (Aeroporto)
        if (abs(polegar_ponta[1] - mindinho_ponta[1]) < 30 and  # Mão plana
            abs(indicador_ponta[1] - medio_ponta[1]) < 20):
            return "aeroporto"
        
        # Gesto: MÃO OSCILANDO (Onde)
        if len(self.historico_gestos) > 3:
            ultimos_gestos = self.historico_gestos[-3:]
            if all(g == "movimento" for g in ultimos_gestos):
                return "onde"
        
        return None
    
    def _detectar_movimento(self, landmarks):
        """Detecta movimento geral da mão"""
        if not hasattr(self, 'landmarks_anterior') or self.landmarks_anterior is None:
            self.landmarks_anterior = landmarks
            return "movimento"
        
        # Calcular movimento médio
        movimento_total = 0
        pontos_compare = min(len(landmarks), len(self.landmarks_anterior))
        
        for i in range(pontos_compare):
            mov_x = abs(landmarks[i][0] - self.landmarks_anterior[i][0])
            mov_y = abs(landmarks[i][1] - self.landmarks_anterior[i][1])
            movimento_total += mov_x + mov_y
        
        self.landmarks_anterior = landmarks
        
        if movimento_total > 100:  # Threshold para movimento significativo
            return "movimento"
        
        return None
    
    def obter_frame(self):
        """Obtém e processa o frame atual da câmera"""
        if not self.ativa:
            return None
            
        if self.cap and self.cap.isOpened():
            # Câmera real
            ret, frame = self.cap.read()
            if ret:
                # Processar com MediaPipe
                frame_processado, gesto, landmarks = self._processar_frame_mediapipe(frame)
                
                # Adicionar informações ao frame
                frame_com_info = self._adicionar_overlay(frame_processado, gesto, landmarks)
                
                # Converter para superficie pygame
                frame_rgb = cv2.cvtColor(frame_com_info, cv2.COLOR_BGR2RGB)
                frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
                self.frame_atual = pygame.transform.flip(frame_surface, True, False)
                
                # Detectar gesto
                if gesto:
                    self._processar_gesto_detectado(gesto)
                elif landmarks:
                    movimento = self._detectar_movimento(landmarks[0])
                    if movimento:
                        self._processar_gesto_detectado(movimento)
        else:
            # Câmera simulada
            self._atualizar_frame_simulado()
            
        return self.frame_atual
    
    def _adicionar_overlay(self, frame, gesto, landmarks):
        """Adiciona overlay informativo ao frame"""
        h, w = frame.shape[:2]
        
        # Adicionar texto de status
        status_text = "MAOS DETECTADAS" if landmarks else "FAÇA SINAIS DE LIBRAS"
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Adicionar gesto detectado
        if gesto:
            cv2.putText(frame, f"GESTO: {gesto.upper()}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Adicionar retângulo de detecção
        cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (255, 255, 0), 2)
        cv2.putText(frame, "ZONA DE SINAIS", (w//4, h//4 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Instruções
        instrucoes = [
            "SINAIS: Onibus, Terminal, Qual",
            "Horas, Centro, Aeroporto, Onde"
        ]
        for i, instrucao in enumerate(instrucoes):
            cv2.putText(frame, instrucao, (10, h - 30 - i*25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def _processar_gesto_detectado(self, gesto):
        """Processa gesto detectado com filtro temporal"""
        tempo_atual = time.time()
        
        # Evitar detecções muito rápidas
        if tempo_atual - self.ultimo_sinal_tempo < 2.0:
            return
        
        # Adicionar ao histórico
        self.historico_gestos.append(gesto)
        if len(self.historico_gestos) > self.max_historico:
            self.historico_gestos.pop(0)
        
        # Só considerar gestos estáveis (aparecem múltiplas vezes)
        if len(self.historico_gestos) >= 3:
            ultimos_3 = self.historico_gestos[-3:]
            if all(g == gesto for g in ultimos_3) and gesto != "movimento":
                self.sinal_atual = gesto
                self.ultimo_sinal_tempo = tempo_atual
                print(f"👐 GESTO CONFIRMADO: {gesto}")
    
    def _atualizar_frame_simulado(self):
        """Atualiza frame simulado com visualização de detecção"""
        if self.frame_atual:
            # Fundo
            self.frame_atual.fill((50, 50, 100))
            largura, altura = self.frame_atual.get_size()
            
            # Zona de detecção
            pygame.draw.rect(self.frame_atual, (255, 255, 0), 
                           (largura//4, altura//4, largura//2, altura//2), 2)
            
            # Mãos simuladas
            tempo = time.time()
            for i in range(2):
                x = largura//2 + int(100 * math.sin(tempo * 2 + i * 3.14))
                y = altura//2 + int(50 * math.cos(tempo * 3 + i * 1.57))
                
                # Desenhar mão simulada
                pygame.draw.circle(self.frame_atual, (0, 255, 0), (x, y), 20)
                for j in range(5):
                    angulo = j * 0.5 + tempo * 2
                    dedo_x = x + int(30 * math.sin(angulo))
                    dedo_y = y + int(30 * math.cos(angulo))
                    pygame.draw.circle(self.frame_atual, (0, 200, 100), (dedo_x, dedo_y), 8)
            
            # Texto informativo
            fonte = pygame.font.SysFont('Arial', 20)
            texto = fonte.render("DETECÇÃO SIMULADA - MOVE AS MAOS", True, (255, 255, 255))
            self.frame_atual.blit(texto, (largura//2 - 150, 20))
            
            if self.sinal_atual:
                sinal_texto = fonte.render(f"SINAL: {self.sinal_atual.upper()}", True, (0, 255, 0))
                self.frame_atual.blit(sinal_texto, (largura//2 - 80, altura - 40))
    
    def obter_sinal_detectado(self):
        """Retorna o sinal detectado e limpa para próxima detecção"""
        if self.sinal_atual:
            sinal = self.sinal_atual
            self.sinal_atual = None
            return sinal
        return None
    
    def parar_camera(self):
        """Para a câmera e libera recursos"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.hands:
            self.hands.close()
        self.ativa = False
        print("📷 Câmera e reconhecimento parados")
    
    def esta_ativa(self):
        return self.ativa
    
    def __del__(self):
        """Destrutor"""
        self.parar_camera()

# Alias para compatibilidade
ReconhecimentoLibrasCamera = ReconhecimentoLibras