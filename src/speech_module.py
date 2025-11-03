import threading
import time
import random

class ReconhecimentoVoz:
    def __init__(self):
        print("✅ Módulo de voz inicializado (Modo Simulação Avançada)")
        self.ouvindo = False
        self.resultado = None
        self.em_processamento = False
        
        # Lista de perguntas simuladas mais realistas
        self.perguntas = [
            "qual ônibus vai para o terminal",
            "que horas chega o seiscentos e quarenta",
            "ônibus para o centro",
            "informações do trezentos e seis",
            "linha para o aeroporto",
            "qual ônibus vai para a cidade nova",
            "horário do oitocentos e quinze",
            "onde pego o ônibus para o centro",
            "que ônibus vai para o terminal três",
            "informações da linha cento e vinte"
        ]
        self.indice_pergunta = 0
        self.microfone_disponivel = False  # PyAudio não disponível

    def iniciar_escuta(self):
        """Inicia escuta simulada"""
        if self.ouvindo or self.em_processamento:
            return False
        
        self.ouvindo = True
        self.em_processamento = True
        self.resultado = None
        
        print("🎤 Modo simulação - Processando pergunta...")
        threading.Thread(target=self._processar_escuta_simulada, daemon=True).start()
        return True

    def _processar_escuta_simulada(self):
        """Processa escuta simulada com feedback visual"""
        # Simular tempo de escuta
        for i in range(3):
            print(f"🎤 Escutando... {i+1}/3")
            time.sleep(1)
        
        # Usar perguntas em sequência
        pergunta = self.perguntas[self.indice_pergunta]
        self.indice_pergunta = (self.indice_pergunta + 1) % len(self.perguntas)
        
        print(f"✅ Reconhecido: '{pergunta}'")
        self.resultado = pergunta
        
        self.ouvindo = False
        self.em_processamento = False

    def obter_resultado(self):
        """Retorna o resultado se disponível"""
        if self.resultado is not None:
            resultado = self.resultado
            self.resultado = None
            return resultado
        return None

    def esta_ouvindo(self):
        """Retorna se está ouvindo no momento"""
        return self.ouvindo

    def parar_escuta(self):
        """Para a escuta"""
        self.ouvindo = False
        self.em_processamento = False
        self.resultado = None

# Versão fallback mantida para compatibilidade
class ReconhecimentoVozFallback(ReconhecimentoVoz):
    def __init__(self):
        super().__init__()
        print("🔧 Usando fallback de voz")