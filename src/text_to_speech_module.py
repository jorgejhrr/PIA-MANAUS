from gtts import gTTS
import pygame
import threading
import os
import tempfile

class SinteseVoz:
    def __init__(self):
        pygame.mixer.init()
        self.playing = False
        
    def falar(self, texto):
        """Fala o texto usando gTTS em thread separada"""
        if self.playing:
            return
            
        thread = threading.Thread(target=self._falar_thread, args=(texto,), daemon=True)
        thread.start()
    
    def _falar_thread(self, texto):
        """Processa a fala em thread separada"""
        try:
            self.playing = True
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                temp_path = tmp_file.name
            
            # Gerar áudio com gTTS
            tts = gTTS(text=texto, lang='pt-br', slow=False)
            tts.save(temp_path)
            
            # Reproduzir com pygame
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Esperar terminar de tocar
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
            # Limpar
            pygame.mixer.music.unload()
            os.unlink(temp_path)
            self.playing = False
            
        except Exception as e:
            print(f"❌ Erro na síntese de voz: {e}")
            self.playing = False

# Fallback simples
class SinteseVozFallback:
    def falar(self, texto):
        print(f"🔊 TTS: {texto}")