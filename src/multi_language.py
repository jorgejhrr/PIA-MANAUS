class MultiLanguage:
    def __init__(self):
        self.current_language = "pt"
        self.supported_languages = {
            "pt": "Português",
            "en": "English", 
            "es": "Español"
        }
    
    def set_language(self, language_code):
        """Altera o idioma atual"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key):
        """Obtém texto traduzido"""
        translations = {
            "pt": {
                "welcome": "Olá! Como posso ajudar?",
                "listening": "Estou ouvindo...",
                "processing": "Processando sua pergunta...",
                "sorry": "Desculpe, não entendi"
            },
            "en": {
                "welcome": "Hello! How can I help you?",
                "listening": "I'm listening...", 
                "processing": "Processing your question...",
                "sorry": "Sorry, I didn't understand"
            },
            "es": {
                "welcome": "¡Hola! ¿Cómo puedo ayudarte?",
                "listening": "Estoy escuchando...",
                "processing": "Procesando tu pregunta...", 
                "sorry": "Lo siento, no entendí"
            }
        }
        
        return translations.get(self.current_language, {}).get(key, key)