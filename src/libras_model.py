import json
import re
from datetime import datetime

class LibrasLibrary:
    def __init__(self):
        self.carregar_banco_libras()
        self.carregar_banco_transportes()
        
    def carregar_banco_libras(self):
        """Carrega o banco completo de sinais de Libras validado"""
        self.sinais_libras = {
            # SAUDAÇÕES BÁSICAS
            "olá": "saudação_inicial",
            "oi": "saudação_inicial", 
            "bom dia": "bom_dia",
            "boa tarde": "boa_tarde",
            "boa noite": "boa_noite",
            "obrigado": "agradecimento",
            "por favor": "por_favor",
            
            # PERGUNTAS
            "qual": "interrogacao_qual",
            "quando": "interrogacao_quando",
            "onde": "interrogacao_onde",
            "como": "interrogacao_como",
            "quanto": "interrogacao_quanto",
            "por que": "interrogacao_porque",
            
            # TRANSPORTE
            "ônibus": "onibus",
            "ônibus": "onibus",
            "terminal": "terminal",
            "parada": "parada_onibus",
            "linha": "linha_onibus",
            "horário": "horario",
            "preço": "dinheiro",
            "tarifa": "dinheiro",
            "cartão": "cartao_transporte",
            
            # DESTINOS
            "centro": "centro_cidade",
            "aeroporto": "aeroporto",
            "shopping": "shopping",
            "hospital": "hospital",
            "universidade": "universidade",
            "praça": "praca",
            
            # NÚMEROS (0-100)
            **{str(i): f"numero_{i}" for i in range(101)},
            
            # DIREÇÕES
            "esquerda": "esquerda",
            "direita": "direita", 
            "frente": "frente",
            "atrás": "atras",
            "perto": "perto",
            "longe": "longe",
            
            # TEMPO
            "hoje": "hoje",
            "amanhã": "amanha",
            "agora": "agora",
            "depois": "depois",
            "rápido": "rapido",
            "devagar": "devagar"
        }
        
    def carregar_banco_transportes(self):
        """Carrega banco de dados de transportes"""
        self.info_transporte = {
            "linhas": {
                "306": {"nome": "Centro-Zona Leste", "frequencia": "15min", "operacao": "5h-23h"},
                "640": {"nome": "T1-T3 Expresso", "frequencia": "20min", "operacao": "5:30h-22:30h"},
                "120": {"nome": "Zona Oeste-Centro", "frequencia": "25min", "operacao": "5h-22h"},
                "815": {"nome": "Aeroporto-Zona Sul", "frequencia": "30min", "operacao": "5:15h-23:15h"},
                "402": {"nome": "Alvorada-Centro", "frequencia": "35min", "operacao": "5:10h-22:10h"},
                "702": {"nome": "Aeroporto Expresso", "frequencia": "40min", "operacao": "5:20h-22:20h"}
            },
            "terminais": {
                "t1": "Terminal 1 - Centro",
                "t2": "Terminal 2 - Zona Leste", 
                "t3": "Terminal 3 - Zona Sul",
                "t4": "Terminal 4 - Zona Oeste"
            },
            "tarifas": {
                "inteira": 4.50,
                "meia": 2.25,
                "gratuito": "Idosos e PCD"
            }
        }
    
    def interpretar_sinais(self, sinais):
        """Interpreta sequência de sinais em pergunta"""
        sinais = sinais.lower()
        
        # Mapeamento de combinações de sinais para perguntas
        combinacoes = {
            ("qual", "onibus", "terminal"): "qual onibus vai para o terminal",
            ("qual", "onibus", "centro"): "qual onibus vai para o centro",
            ("qual", "onibus", "aeroporto"): "qual onibus vai para o aeroporto",
            ("onde", "pego", "onibus"): "onde pego o onibus",
            ("que", "horas", "onibus"): "que horas passa o onibus",
            ("quanto", "custa", "onibus"): "quanto custa a passagem de onibus",
            ("preciso", "ir", "centro"): "preciso ir para o centro",
            ("como", "chego", "aeroporto"): "como chego no aeroporto",
            ("todas", "linhas"): "quais são todas as linhas de onibus",
            ("horario", "onibus"): "qual o horario do onibus"
        }
        
        for combinacao, pergunta in combinacoes.items():
            if all(sinal in sinais for sinal in combinacao):
                return pergunta
        
        # Fallback: retorna os sinais como pergunta
        return f"pergunta sobre {sinais}"
    
    def gerar_resposta_inteligente(self, pergunta):
        """Gera resposta inteligente baseada na pergunta"""
        pergunta = pergunta.lower()
        
        # Análise de intenção
        if self.contem_todas_linhas(pergunta):
            return self.gerar_resposta_todas_linhas()
        
        elif self.contem_linha_especifica(pergunta):
            return self.gerar_resposta_linha_especifica(pergunta)
        
        elif self.contem_horario(pergunta):
            return self.gerar_resposta_horario(pergunta)
        
        elif self.contem_tarifa(pergunta):
            return self.gerar_resposta_tarifa()
        
        elif self.contem_localizacao(pergunta):
            return self.gerar_resposta_localizacao(pergunta)
        
        else:
            return self.gerar_resposta_generica(pergunta)
    
    def contem_todas_linhas(self, pergunta):
        return any(termo in pergunta for termo in [
            "todas as linhas", "todas linhas", "quais linhas", "linhas disponíveis",
            "lista de onibus", "onibus que tem"
        ])
    
    def contem_linha_especifica(self, pergunta):
        return any(linha in pergunta for linha in self.info_transporte["linhas"].keys())
    
    def contem_horario(self, pergunta):
        return any(termo in pergunta for termo in [
            "horário", "horarios", "que horas", "quando passa", "que hora"
        ])
    
    def contem_tarifa(self, pergunta):
        return any(termo in pergunta for termo in [
            "preço", "quanto custa", "tarifa", "valor", "custa", "passagem"
        ])
    
    def contem_localizacao(self, pergunta):
        return any(termo in pergunta for termo in [
            "onde", "local", "fica", "parada", "terminal", "como chego", "como ir"
        ])
    
    def gerar_resposta_todas_linhas(self):
        """Gera resposta completa sobre todas as linhas"""
        linhas_info = []
        for num, info in self.info_transporte["linhas"].items():
            linhas_info.append(f"• {num} - {info['nome']} ({info['operacao']})")
        
        return "🚍 TODAS AS LINHAS DE ÔNIBUS:\n" + "\n".join(linhas_info) + \
               "\n\n💡 Use o MODO MAPA para ver paradas!"
    
    def gerar_resposta_linha_especifica(self, pergunta):
        """Gera resposta para linha específica"""
        for num, info in self.info_transporte["linhas"].items():
            if num in pergunta:
                return f"🚍 LINHA {num}:\n{info['nome']}\n⏰ {info['operacao']}\n🔄 {info['frequencia']}"
        
        return "Linha não encontrada. Pergunte sobre: 306, 640, 120, 815, 402, 702"
    
    def gerar_resposta_horario(self, pergunta):
        """Gera resposta sobre horários"""
        hora_atual = datetime.now().strftime("%H:%M")
        return f"⏰ HORÁRIOS:\nAgora são {hora_atual}\nÔnibus operam das 5h às 23h\nFrequência: 15-40min\nPergunte por uma linha específica!"
    
    def gerar_resposta_tarifa(self):
        """Gera resposta sobre tarifas"""
        tarifas = self.info_transporte["tarifas"]
        return f"💰 TARIFAS:\n• Inteira: R$ {tarifas['inteira']}\n• Meia: R$ {tarifas['meia']}\n• Gratuito: {tarifas['gratuito']}"
    
    def gerar_resposta_localizacao(self, pergunta):
        """Gera resposta sobre localização"""
        return "📍 Use o MODO MAPA para ver:\n• Todas as paradas\n• Terminais\n• Rotas exatas\n• Localização em tempo real!"
    
    def gerar_resposta_generica(self, pergunta):
        """Resposta genérica inteligente"""
        respostas_genericas = [
            "Posso ajudar com informações sobre linhas de ônibus, horários, tarifas e localizações!",
            "Sou especializado em transporte de Manaus. Pergunte sobre ônibus!",
            "Use MODO MAPA para ver paradas ou pergunte sobre linhas específicas!",
            "Posso informar sobre as linhas 306, 640, 120, 815, 402, 702 e outras!"
        ]
        
        # Análise simples de contexto
        if "obrigado" in pergunta:
            return "De nada! Estou aqui para ajudar."
        elif "ajuda" in pergunta:
            return "Posso ajudar com: linhas de ônibus, horários, tarifas, localização de paradas!"
        
        import random
        return random.choice(respostas_genericas)
    
    def obter_sinal_libras(self, palavra):
        """Retorna o sinal de Libras para uma palavra"""
        return self.sinais_libras.get(palavra.lower(), "sinal_generico")
    
    def traduzir_frase_libras(self, frase):
        """Traduz frase completa para sequência de sinais"""
        palavras = frase.split()
        sinais = []
        
        for palavra in palavras:
            sinal = self.obter_sinal_libras(palavra)
            if sinal:
                sinais.append(sinal)
        
        return sinais