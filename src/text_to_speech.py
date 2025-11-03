from gtts import gTTS
import pygame
import io
import tempfile
import os

class TextToSpeech:
    def __init__(self):
        pygame.mixer.init()
    
    def speak(self, text):
        """Converte texto em fala"""
        try:
            print(f"🔊 Falando: {text}")
            tts = gTTS(text=text, lang='pt-br')
            
            # Criar arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Reproduzir áudio
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Esperar terminar de tocar
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Limpar arquivo temporário
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"⚠️  Erro na síntese de voz: {e}")