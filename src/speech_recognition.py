import speech_recognition as sr

class SpeechRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrar para ruído ambiente
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except:
            print("⚠️  Microfone não disponível. Usando modo simulado.")
    
    def listen(self):
        """Ouve e reconhece fala do usuário"""
        try:
            print("🎤 Ouvindo... Fale agora!")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("🔄 Processando...")
            text = self.recognizer.recognize_google(audio, language='pt-BR')
            print(f"👤 Você disse: {text}")
            return text.lower()
        
        except sr.WaitTimeoutError:
            print("⏰ Tempo esgotado para falar")
            return None
        except sr.UnknownValueError:
            print("❌ Não foi possível entender o áudio")
            return None
        except Exception as e:
            print(f"⚠️  Erro no reconhecimento: {e}")
            # Modo simulado para teste
            return self.simulated_listen()
    
    def simulated_listen(self):
        """Modo simulado quando o microfone não está disponível"""
        simulated_questions = [
            "qual ônibus vai para o terminal 3",
            "que horas chega o 640", 
            "ônibus para o centro",
            "linha para o aeroporto"
        ]
        
        import random
        question = random.choice(simulated_questions)
        print(f"🎮 Modo simulado: '{question}'")
        return question