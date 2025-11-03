import pygame
import sys
import os
import webbrowser
import time
import threading

# Adicionar nossos próprios módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# CARREGAMENTO ROBUSTO DE MÓDULOS
MODULOS_CARREGADOS = True

try:
    from speech_module import ReconhecimentoVoz
    print("✅ Módulo de voz carregado")
except ImportError as e:
    print(f"❌ Módulo de voz não carregado: {e}")
    from speech_module import ReconhecimentoVozFallback as ReconhecimentoVoz

try:
    from text_to_speech_module import SinteseVoz
    print("✅ Módulo TTS carregado")
except ImportError as e:
    print(f"❌ Módulo TTS não carregado: {e}")
    # Criar fallback
    class SinteseVoz:
        def falar(self, texto): 
            print(f"🔊 TTS: {texto}")

try:
    from database_module import BancoDadosOnibus
    print("✅ Módulo banco de dados carregado")
except ImportError as e:
    print(f"❌ Módulo BD não carregado: {e}")
    # Criar fallback
    class BancoDadosOnibus:
        def obter_info_linha(self, num): 
            return [num, f"Linha {num}", "Terminal", "Centro", "06:00-22:00"]
        def obter_onibus_para_destino(self, dest): 
            return [["640", "Linha 640"], ["306", "Linha 306"]]

try:
    from avatar_libras import AvatarLibras
    print("✅ Módulo avatar carregado")
except ImportError as e:
    print(f"❌ Módulo avatar não carregado: {e}")
    # Criar fallback
    class AvatarLibras:
        def iniciar_sequencia(self, texto): 
            print(f"👐 Avatar: {texto}")
        def atualizar(self): 
            pass
        def desenhar(self, screen, x, y, w, h): 
            pygame.draw.rect(screen, (70, 70, 120), (x, y, w, h))
            fonte = pygame.font.SysFont('Arial', 20)
            texto = fonte.render("AVATAR LIBRAS", True, (255,255,255))
            screen.blit(texto, (x + 50, y + 50))

try:
    from camera_libras import ReconhecimentoLibrasCamera
    print("✅ Módulo câmera carregado")
except ImportError as e:
    print(f"❌ Módulo câmera não carregado: {e}")
    # Criar fallback
    class ReconhecimentoLibrasCamera:
        def __init__(self):
            self.ativa = False
            self.frame_atual = None
        def iniciar_camera(self): 
            print("📷 Câmera simulada")
            self.ativa = True
            return True
        def parar_camera(self): 
            self.ativa = False
        def esta_ativa(self): 
            return self.ativa
        def obter_frame(self): 
            return None
        def obter_sinal_detectado(self): 
            return None

class PIAManaus:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("PIA Manaus - Reconhecimento Real de Libras")
        self.clock = pygame.time.Clock()
        
        # Inicializar módulos
        self.reconhecimento_voz = ReconhecimentoVoz()
        self.sintese_voz = SinteseVoz()
        self.banco_dados = BancoDadosOnibus()
        self.avatar_libras = AvatarLibras()
        self.camera_libras = ReconhecimentoLibrasCamera()
        self.modulos_ativos = True
        
        self.running = True
        self.mensagem_status = "PIA Manaus - Sistema Carregado! Clique em CÂMERA LIBRAS."
        self.cor_status = (255, 255, 0)
        self.informacoes_extras = ""
        self.mostrar_avatar = False
        self.mostrar_camera = False
        self.resposta_atual = ""
        self.ultima_pergunta = ""
        self.pergunta_usuario = ""
        self.estado_voz = "parado"
        self.sinais_detectados = []
        
        # Cores
        self.cor_fundo = (0, 51, 102)
        self.cor_texto = (255, 255, 255)
        
        # Fontes
        self.fonte_grande = pygame.font.SysFont('Arial', 36, bold=True)
        self.fonte_media = pygame.font.SysFont('Arial', 24)
        self.fonte_pequena = pygame.font.SysFont('Arial', 18)
        self.fonte_muito_pequena = pygame.font.SysFont('Arial', 14)
        
        # Timer para animações
        self.tempo_animacao = 0
        
        print("✅ Sistema PIA Manaus com Reconhecimento Real de Libras iniciado!")
    
    def run(self):
        """Loop principal"""
        while self.running:
            self.tempo_animacao += 1
            
            self.processar_eventos()
            self.atualizar_sistema()
            self.desenhar_interface()
            
            self.clock.tick(60)
        
        # Limpar recursos
        if hasattr(self.camera_libras, 'esta_ativa') and self.camera_libras.esta_ativa():
            self.camera_libras.parar_camera()
        
        pygame.quit()
        sys.exit()
    
    def processar_eventos(self):
        """Processa eventos do pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.processar_teclas(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.processar_clique_mouse()
    
    def processar_teclas(self, tecla):
        if tecla == pygame.K_ESCAPE:
            self.running = False
        elif tecla == pygame.K_v:
            self.ativar_modo_voz()
        elif tecla == pygame.K_m:
            self.ativar_modo_mapa()
        elif tecla == pygame.K_c:
            self.ativar_modo_camera()
        elif tecla == pygame.K_l:
            self.ativar_modo_libras()
        elif tecla == pygame.K_i:
            self.mostrar_info_sistema()
    
    def processar_clique_mouse(self):
        pos = pygame.mouse.get_pos()
        botoes = self.criar_botoes()
        
        for nome_botao, retangulo in botoes.items():
            if retangulo.collidepoint(pos):
                if nome_botao == "voz":
                    self.ativar_modo_voz()
                elif nome_botao == "mapa":
                    self.ativar_modo_mapa()
                elif nome_botao == "camera":
                    self.ativar_modo_camera()
                elif nome_botao == "libras":
                    self.ativar_modo_libras()
                elif nome_botao == "info":
                    self.mostrar_info_sistema()
                break
    
    def atualizar_sistema(self):
        """Atualiza estados do sistema"""
        # Atualizar avatar
        if self.mostrar_avatar:
            self.avatar_libras.atualizar()
        
        # Atualizar câmera e detectar sinais EM TEMPO REAL
        if self.mostrar_camera:
            if not self.camera_libras.esta_ativa():
                if not self.camera_libras.iniciar_camera():
                    self.mensagem_status = "❌ Câmera não disponível"
                    self.mostrar_camera = False
        
            # Processar frame da câmera (já inclui detecção em tempo real)
            self.camera_libras.obter_frame()
            
            # Verificar sinais detectados (agora em tempo real)
            sinal = self.camera_libras.obter_sinal_detectado()
            if sinal:
                self.processar_sinal_libras(sinal)
    
        # Verificar resultado de voz
        if self.estado_voz == "ouvindo":
            resultado = self.reconhecimento_voz.obter_resultado()
            if resultado is not None:
                self.processar_resultado_voz(resultado)
                self.estado_voz = "parado"
            elif not self.reconhecimento_voz.esta_ouvindo():
                self.estado_voz = "parado"
                self.mensagem_status = "⏰ Tempo esgotado. Tente novamente."
                self.cor_status = (255, 100, 0)
    
    def ativar_modo_camera(self):
        """Ativa modo câmera para reconhecimento de Libras"""
        if self.mostrar_camera:
            # Já está ativo, desativar
            self.camera_libras.parar_camera()
            self.mostrar_camera = False
            self.mensagem_status = "📷 Modo Câmera Desativado"
            self.cor_status = (255, 255, 0)
            self.informacoes_extras = ""
        else:
            # Ativar modo câmera
            self.mensagem_status = "📷 INICIANDO CÂMERA COM RECONHECIMENTO DE LIBRAS..."
            self.cor_status = (255, 255, 0)
            
            if self.camera_libras.iniciar_camera():
                self.mostrar_camera = True
                self.mostrar_avatar = False
                self.estado_voz = "parado"
                self.mensagem_status = "📷 CÂMERA ATIVA - FAÇA GESTOS DE LIBRAS!"
                self.cor_status = (0, 200, 255)
                self.sinais_detectados = []
                
                self.informacoes_extras = """
📷 CÂMERA COM RECONHECIMENTO REAL DE LIBRAS!

🎯 GESTOS RECONHECIDOS:
• 🚍 ÔNIBUS: Polegar para cima
• 🏢 TERMINAL: Mão aberta  
• ❓ QUAL: Indicador para cima
• ⏰ HORAS: Apontar para pulso
• 📍 CENTRO: Apontar para centro
• 🛫 AEROPORTO: Mão plana
• 📍 ONDE: Movimento oscilatório

💡 COMO USAR:
1. Posicione as mãos na ZONA DE SINAIS
2. Faça gestos claros e pausados
3. Aguarde a confirmação visual
4. Sistema detecta automaticamente

👐 DICA: Mantenha os gestos por 2-3 segundos
                """
            else:
                self.mensagem_status = "❌ Erro ao iniciar câmera"
                self.cor_status = (255, 0, 0)
                self.informacoes_extras = "Verifique se a câmera está conectada e tente novamente."
    
    def processar_sinal_libras(self, sinal):
        """Processa sinal de Libras detectado pela câmera"""
        # Evitar processar o mesmo sinal repetidamente
        if self.sinais_detectados and self.sinais_detectados[-1] == sinal:
            return
            
        self.sinais_detectados.append(sinal)
        
        # Limitar quantidade de sinais
        if len(self.sinais_detectados) > 5:
            self.sinais_detectados = self.sinais_detectados[-5:]
        
        self.mensagem_status = f"👐 GESTO DETECTADO: {sinal.upper()}"
        self.cor_status = (0, 255, 255)
        
        # Feedback visual imediato
        self.informacoes_extras = f"✅ Gesto '{sinal}' confirmado! Continue fazendo gestos..."
        
        # Se temos sinais suficientes, formar pergunta
        if len(self.sinais_detectados) >= 2:
            pergunta = self.formar_pergunta_libras()
            self.processar_pergunta_libras(pergunta)
    
    def formar_pergunta_libras(self):
        """Forma uma pergunta a partir dos sinais detectados"""
        sinais = " ".join(self.sinais_detectados)
        
        # Mapear combinações de sinais para perguntas
        if "qual" in sinais and "onibus" in sinais and "terminal" in sinais:
            return "qual onibus vai para o terminal"
        elif "qual" in sinais and "onibus" in sinais and "centro" in sinais:
            return "qual onibus vai para o centro"
        elif "qual" in sinais and "onibus" in sinais and "aeroporto" in sinais:
            return "qual onibus vai para o aeroporto"
        elif "horas" in sinais and "onibus" in sinais:
            return "que horas chega o onibus"
        elif "onde" in sinais and "onibus" in sinais:
            return "onde pego o onibus"
        elif "640" in sinais or "306" in sinais or "120" in sinais or "815" in sinais:
            for numero in ["640", "306", "120", "815"]:
                if numero in sinais:
                    return f"informacoes do onibus {numero}"
        
        # Combinações simples
        if "onibus" in sinais and "terminal" in sinais:
            return "onibus para o terminal"
        elif "onibus" in sinais and "centro" in sinais:
            return "onibus para o centro"
        elif "onibus" in sinais and "aeroporto" in sinais:
            return "onibus para o aeroporto"
        
        return f"pergunta sobre {sinais}"
    
    def processar_pergunta_libras(self, pergunta):
        """Processa pergunta feita por Libras"""
        self.ultima_pergunta = pergunta
        self.pergunta_usuario = f"[LIBRAS] {pergunta}"
        
        self.mensagem_status = "🤔 PROCESSANDO GESTOS DE LIBRAS..."
        self.cor_status = (255, 255, 0)
        
        resposta = self.gerar_resposta(pergunta)
        self.resposta_atual = resposta
        
        # Ativar avatar para responder em Libras
        self.mostrar_avatar = True
        self.avatar_libras.iniciar_sequencia(resposta)
        self.sintese_voz.falar(resposta)
        
        self.mensagem_status = "💡 RESPOSTA EM LIBRAS!"
        self.cor_status = (0, 255, 0)
        
        self.informacoes_extras = f"""
📷 PERGUNTA POR LIBRAS:
{pergunta}

🎯 RESPOSTA:
{resposta}

👐 AVATAR RESPONDENDO EM LIBRAS
🔊 ÁUDIO ATIVO

💡 Continue fazendo gestos para novas perguntas!
        """
        
        # Limpar sinais após processar
        self.sinais_detectados = []
    
    def ativar_modo_voz(self):
        """Ativa modo voz"""
        if self.estado_voz == "parado":
            # Desativar câmera se estiver ativa
            if self.mostrar_camera:
                self.camera_libras.parar_camera()
                self.mostrar_camera = False
            
            # Iniciar escuta com tratamento de erro
            try:
                if self.reconhecimento_voz.iniciar_escuta():
                    self.estado_voz = "ouvindo"
                    self.mensagem_status = "🎤 OUVINDO... FALE AGORA!"
                    self.cor_status = (0, 255, 0)
                    self.informacoes_extras = ""
                    self.mostrar_avatar = False
                else:
                    self.mensagem_status = "❌ Sistema de voz ocupado"
                    self.cor_status = (255, 100, 0)
            except Exception as e:
                print(f"❌ Erro ao iniciar escuta: {e}")
                self.mensagem_status = "❌ Erro no sistema de voz"
                self.cor_status = (255, 0, 0)
    
    def processar_resultado_voz(self, pergunta):
        """Processa resultado do reconhecimento de voz"""
        if not pergunta:
            self.estado_voz = "parado"
            self.mensagem_status = "❌ Não entendi. Tente novamente."
            self.cor_status = (255, 0, 0)
            return
        
        self.estado_voz = "processando"
        self.ultima_pergunta = pergunta
        self.pergunta_usuario = pergunta
        
        resposta = self.gerar_resposta(pergunta)
        self.resposta_atual = resposta
        
        # Ativar avatar para resposta em Libras
        self.mostrar_avatar = True
        self.avatar_libras.iniciar_sequencia(resposta)
        self.sintese_voz.falar(resposta)
        
        self.estado_voz = "parado"
        self.mensagem_status = "💡 RESPOSTA PRONTA!"
        self.cor_status = (0, 255, 0)
        
        self.informacoes_extras = f"""
📝 PERGUNTA: "{pergunta}"

🎯 RESPOSTA: {resposta}

👐 AVATAR: Mostrando resposta em Libras
🔊 ÁUDIO: Resposta em andamento
        """
    
    def ativar_modo_mapa(self):
        """Ativa modo mapa"""
        self.mensagem_status = "🗺️ Abrindo Google Maps..."
        self.cor_status = (255, 165, 0)
        self.mostrar_avatar = False
        self.mostrar_camera = False
        self.estado_voz = "parado"
        
        if self.camera_libras.esta_ativa():
            self.camera_libras.parar_camera()
        
        try:
            webbrowser.open("https://www.google.com/maps/place/Manaus,+AM/")
            self.mensagem_status = "🗺️ Google Maps aberto!"
            
            threading.Thread(target=lambda: self.sintese_voz.falar("Google Maps aberto"), daemon=True).start()
                
            self.informacoes_extras = """
📍 MAPA DE MANAUS ABERTO!

🎯 Terminais disponíveis:
• Terminal 1, 2 e 3
• Centro da cidade
• Aeroporto

💡 Use a busca para encontrar ônibus
"""
        except Exception:
            self.mensagem_status = "❌ Erro ao abrir mapa"
            self.cor_status = (255, 0, 0)
    
    def ativar_modo_libras(self):
        """Ativa modo libras do avatar"""
        self.mensagem_status = "👐 MODO AVATAR LIBRAS ATIVADO!"
        self.cor_status = (128, 0, 128)
        self.mostrar_avatar = True
        self.mostrar_camera = False
        self.estado_voz = "parado"
        
        if self.camera_libras.esta_ativa():
            self.camera_libras.parar_camera()
        
        threading.Thread(target=lambda: self.sintese_voz.falar("Modo Avatar Libras ativado"), daemon=True).start()
        
        if self.ultima_pergunta:
            self.avatar_libras.iniciar_sequencia(self.resposta_atual)
        else:
            self.avatar_libras.iniciar_sequencia("Como posso ajudar com informações de ônibus?")
        
        self.informacoes_extras = """
🎯 MODO AVATAR LIBRAS

👀 Avatar mostrando sinais:

• Respostas visuais em Libras
• Para deficientes auditivos
• Sincronizado com áudio

💡 Faça perguntas por voz ou câmera!
"""
    
    def mostrar_info_sistema(self):
        """Mostra informações do sistema"""
        self.mensagem_status = "📊 SISTEMA PIA MANAUS - RECONHECIMENTO REAL DE LIBRAS"
        self.cor_status = (0, 255, 255)
        self.mostrar_avatar = False
        self.mostrar_camera = False
        self.estado_voz = "parado"
        
        if self.camera_libras.esta_ativa():
            self.camera_libras.parar_camera()
        
        threading.Thread(target=lambda: self.sintese_voz.falar("Sistema PIA Manaus com reconhecimento real de Libras por câmera"), daemon=True).start()
        
        self.informacoes_extras = """
🔧 PIA MANAUS - RECONHECIMENTO REAL DE LIBRAS

✅ TECNOLOGIA:
• 📷 MediaPipe Hands - Detecção de mãos em tempo real
• 👐 21 pontos de landmark por mão
• 🤖 IA para reconhecimento de gestos
• ⚡ Processamento em tempo real

🎯 GESTOS RECONHECIDOS:
• Ônibus, Terminal, Qual, Horas
• Centro, Aeroporto, Onde

🚍 DADOS DE MANAUS:
• 5 linhas de ônibus reais
• Terminais e horários
• Rotas atualizadas

👥 ACESSIBILIDADE COMPLETA:
• Deficientes auditivos: Libras por câmera
• Deficientes visuais: Voz e áudio
• Interface universal inclusiva
"""
    
    def gerar_resposta(self, pergunta):
        """Gera resposta para perguntas"""
        pergunta = pergunta.lower()
        
        # Busca por números de ônibus
        for numero in ['640', '306', '120', '815', '611']:
            if numero in pergunta:
                info = self.banco_dados.obter_info_linha(numero)
                if info:
                    return f"Ônibus {info[0]} - {info[1]}. De {info[2]} para {info[3]}. Horário: {info[4]}."
                return f"Ônibus {numero} - Informações disponíveis."
        
        # Busca por destinos
        destinos = ['terminal', 'centro', 'aeroporto', 'flores', 'cidade nova', 'japiim']
        for destino in destinos:
            if destino in pergunta:
                onibus = self.banco_dados.obter_onibus_para_destino(destino)
                if onibus:
                    lista = ", ".join([f"{bus[0]}" for bus in onibus[:3]])
                    return f"Para {destino}, pegue: {lista}."
                return f"Ônibus para {destino} disponíveis."
        
        return "Pergunte sobre linhas de ônibus em Manaus. Exemplos: 'ônibus 640', 'para o terminal', 'linha aeroporto'."
    
    def criar_botoes(self):
        return {
            "voz": pygame.Rect(50, 200, 200, 50),
            "mapa": pygame.Rect(50, 270, 200, 50),
            "camera": pygame.Rect(50, 340, 200, 50),
            "libras": pygame.Rect(50, 410, 200, 50),
            "info": pygame.Rect(50, 480, 200, 50)
        }
    
    def desenhar_interface(self):
        """Desenha interface completa"""
        self.screen.fill(self.cor_fundo)
        
        # Título
        titulo = self.fonte_grande.render("PIA MANAUS - RECONHECIMENTO REAL DE LIBRAS", True, self.cor_texto)
        subtitulo = self.fonte_media.render("Sistema com IA para Detecção de Gestos", True, (200, 200, 200))
        self.screen.blit(titulo, (180, 30))
        self.screen.blit(subtitulo, (320, 80))
        
        # Status
        status = self.fonte_media.render(self.mensagem_status, True, self.cor_status)
        self.screen.blit(status, (50, 140))
        
        # Indicador de atividade
        if self.estado_voz == "ouvindo":
            raio = 8 + (self.tempo_animacao % 30) // 3
            pygame.draw.circle(self.screen, (0, 255, 0), (30, 135), raio, 2)
        
        # Botões
        self.desenhar_botoes()
        
        # Conteúdo principal
        if self.mostrar_camera:
            self.desenhar_camera()
        elif self.mostrar_avatar:
            self.desenhar_avatar()
        else:
            self.desenhar_instrucoes()
        
        # Informações extras
        if self.informacoes_extras:
            self.desenhar_informacoes_extras()
        
        pygame.display.flip()
    
    def desenhar_botoes(self):
        """Desenha botões com estados visuais"""
        botoes = [
            ("VOZ (V)", 50, 200, (0, 150, 0), self.estado_voz != "parado"),
            ("MAPA (M)", 50, 270, (255, 165, 0), False),
            ("CÂMERA (C)", 50, 340, (0, 200, 255), self.mostrar_camera),
            ("AVATAR (L)", 50, 410, (128, 0, 128), self.mostrar_avatar),
            ("INFO (I)", 50, 480, (0, 100, 200), False)
        ]
        
        for texto, x, y, cor, ativo in botoes:
            cor_btn = (min(cor[0] + 40, 255), min(cor[1] + 40, 255), min(cor[2] + 40, 255)) if ativo else cor
            self.desenhar_botao(texto, x, y, cor_btn)
            
            # Indicador de câmera ativa
            if texto == "CÂMERA (C)" and ativo and self.sinais_detectados:
                pygame.draw.circle(self.screen, (255, 255, 0), (x + 190, y + 10), 5)
    
    def desenhar_botao(self, texto, x, y, cor):
        retangulo = pygame.Rect(x, y, 200, 50)
        pygame.draw.rect(self.screen, cor, retangulo, border_radius=10)
        pygame.draw.rect(self.screen, self.cor_texto, retangulo, 2, border_radius=10)
        
        texto_surface = self.fonte_media.render(texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=retangulo.center)
        self.screen.blit(texto_surface, texto_rect)
    
    def desenhar_camera(self):
        """Desenha a câmera com visualização real"""
        # Área da câmera
        camera_rect = pygame.Rect(300, 150, 500, 375)
        pygame.draw.rect(self.screen, (20, 20, 40), camera_rect, border_radius=15)
        pygame.draw.rect(self.screen, (100, 150, 255), camera_rect, 3, border_radius=15)
        
        # Título da câmera
        titulo_camera = self.fonte_pequena.render("📷 CÂMERA COM RECONHECIMENTO DE LIBRAS", True, (0, 255, 255))
        self.screen.blit(titulo_camera, (320, 120))
        
        # Frame da câmera
        frame = self.camera_libras.frame_atual
        if frame:
            # Redimensionar frame para caber na área
            frame_redimensionado = pygame.transform.scale(frame, (480, 360))
            self.screen.blit(frame_redimensionado, (310, 160))
        else:
            # Placeholder se não há frame
            pygame.draw.rect(self.screen, (50, 50, 100), (310, 160, 480, 360))
            texto = self.fonte_media.render("PROCESSANDO CÂMERA...", True, (255, 255, 255))
            self.screen.blit(texto, (380, 300))
            texto2 = self.fonte_pequena.render("Aguarde a inicialização do MediaPipe", True, (200, 200, 255))
            self.screen.blit(texto2, (340, 340))
        
        # Área de sinais detectados
        self.desenhar_area_sinais()

    def desenhar_area_sinais(self):
        """Desenha área de sinais detectados"""
        sinais_rect = pygame.Rect(300, 540, 500, 80)
        pygame.draw.rect(self.screen, (40, 40, 80), sinais_rect, border_radius=10)
        pygame.draw.rect(self.screen, (150, 200, 255), sinais_rect, 2, border_radius=10)
        
        titulo_sinais = self.fonte_pequena.render("GESTOS DETECTADOS:", True, (255, 255, 0))
        self.screen.blit(titulo_sinais, (320, 550))
        
        if self.sinais_detectados:
            ultimos_sinais = self.sinais_detectados[-3:]  # Mostrar últimos 3 sinais
            texto_sinais = self.fonte_pequena.render(
                f"{' → '.join(ultimos_sinais)}", 
                True, (0, 255, 255)
            )
            self.screen.blit(texto_sinais, (320, 580))
            
            # Contador
            contador = self.fonte_muito_pequena.render(
                f"Total: {len(self.sinais_detectados)} gestos", 
                True, (200, 200, 255)
            )
            self.screen.blit(contador, (650, 580))
        else:
            texto_aguarde = self.fonte_pequena.render(
                "Faça gestos de Libras na frente da câmera...", True, (200, 200, 255)
            )
            self.screen.blit(texto_aguarde, (340, 575))
    
    def desenhar_avatar(self):
        """Desenha o avatar e conversa"""
        # Avatar
        avatar_rect = pygame.Rect(300, 150, 500, 250)
        pygame.draw.rect(self.screen, (40, 20, 40), avatar_rect, border_radius=15)
        pygame.draw.rect(self.screen, (150, 100, 150), avatar_rect, 3, border_radius=15)
        
        self.avatar_libras.desenhar(self.screen, 300, 150, 500, 250)
        
        # Conversa
        if self.pergunta_usuario or self.resposta_atual:
            conversa_rect = pygame.Rect(300, 410, 500, 210)
            pygame.draw.rect(self.screen, (30, 50, 80), conversa_rect, border_radius=10)
            pygame.draw.rect(self.screen, (100, 150, 255), conversa_rect, 2, border_radius=10)
            
            y_pos = 425
            if self.pergunta_usuario:
                texto = self.fonte_pequena.render(f"👤: {self.pergunta_usuario}", True, (255, 200, 100))
                self.screen.blit(texto, (320, y_pos))
                y_pos += 30
            
            if self.resposta_atual:
                # Quebrar texto
                palavras = self.resposta_atual.split()
                linhas = []
                linha_atual = ""
                
                for palavra in palavras:
                    if len(linha_atual + palavra) < 50:
                        linha_atual += palavra + " "
                    else:
                        linhas.append(linha_atual)
                        linha_atual = palavra + " "
                if linha_atual:
                    linhas.append(linha_atual)
                
                for i, linha in enumerate(linhas[:4]):
                    texto = self.fonte_pequena.render(f"🤖: {linha}", True, (100, 255, 100))
                    self.screen.blit(texto, (320, y_pos + i * 25))
    
    def desenhar_instrucoes(self):
        """Desenha instruções iniciais"""
        instrucoes = [
            "🎯 SISTEMA COM RECONHECIMENTO REAL DE LIBRAS",
            "",
            "📷 TECNOLOGIA MEDIAPIPE:",
            "• Detecção de 21 pontos por mão",
            "• Reconhecimento de gestos em tempo real",
            "• IA treinada para Libras básica",
            "• Processamento instantâneo",
            "",
            "🎤 RECONHECIMENTO DE VOZ", 
            "• Clique em VOZ e fale naturalmente",
            "• Resposta em áudio e Libras",
            "",
            "👐 GESTOS RECONHECIDOS:",
            "• Ônibus, Terminal, Qual, Horas",
            "• Centro, Aeroporto, Onde"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            cor = (255, 255, 0) if "🎯" in instrucao or "📷" in instrucao or "🎤" in instrucao else (200, 200, 255)
            fonte = self.fonte_pequena
            texto = fonte.render(instrucao, True, cor)
            self.screen.blit(texto, (300, 150 + i * 25))
    
    def desenhar_informacoes_extras(self):
        """Desenha informações extras"""
        info_rect = pygame.Rect(50, 580, 1100, 100)
        pygame.draw.rect(self.screen, (30, 30, 60), info_rect, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 255), info_rect, 2, border_radius=10)
        
        linhas = self.informacoes_extras.strip().split('\n')
        y_pos = 595
        
        for linha in linhas[:6]:
            if linha.strip():
                cor = (255, 255, 0) if any(m in linha for m in ['📷', '🎯', '💡', '👐', '🔊']) else (200, 200, 255)
                texto = self.fonte_muito_pequena.render(linha, True, cor)
                self.screen.blit(texto, (65, y_pos))
                y_pos += 15

if __name__ == "__main__":
    app = PIAManaus()
    app.run()