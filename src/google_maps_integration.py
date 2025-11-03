import webbrowser

class GoogleMapsIntegration:
    def __init__(self):
        self.paradas_manaus = {
            # Terminais Principais
            "Terminal 1 (T1)": "-3.1190,-60.0217",
            "Terminal 2 (T2)": "-3.0746,-59.9865", 
            "Terminal 3 (T3)": "-3.0671,-60.0012",
            "Terminal 4 (T4)": "-3.0964,-59.9648",
            
            # Paradas Estratégicas - Centro
            "Praça da Matriz": "-3.1340,-60.0232",
            "Praça da Polícia": "-3.1315,-60.0248",
            "Av. Eduardo Ribeiro": "-3.1328,-60.0201",
            "Porto de Manaus": "-3.1406,-60.0294",
            
            # Paradas Zona Sul
            "Parque 10": "-3.0996,-60.0265",
            "Aleixo": "-3.0923,-60.0382",
            "Coroado": "-3.1174,-59.9876",
            "Japiim": "-3.0908,-59.9967",
            
            # Paradas Zona Leste
            "Cidade Nova": "-3.0623,-59.9845",
            "Novo Aleixo": "-3.0729,-59.9642",
            "Monte das Oliveiras": "-3.0571,-59.9743",
            
            # Paradas Zona Oeste
            "Compensa": "-3.1156,-60.0498",
            "Glória": "-3.1267,-60.0423",
            "Vila da Prata": "-3.1402,-60.0491",
            
            # Aeroporto e Pontos Turísticos
            "Aeroporto Eduardo Gomes": "-3.0386,-60.0497",
            "Shopping Manaus Via Norte": "-3.0272,-59.9684",
            "Shopping Ponta Negra": "-3.0854,-60.0338",
            "Universidade Federal": "-3.1073,-59.9998"
        }
        
        self.linhas_por_parada = {
            "Terminal 1 (T1)": ["306", "640", "120", "815", "501", "702"],
            "Terminal 2 (T2)": ["306", "120", "402", "515", "625"],
            "Terminal 3 (T3)": ["640", "815", "501", "320", "435"],
            "Terminal 4 (T4)": ["120", "402", "702", "815", "306"],
            "Praça da Matriz": ["306", "640", "120", "402"],
            "Praça da Polícia": ["306", "120", "815", "501"],
            "Av. Eduardo Ribeiro": ["640", "402", "702", "320"],
            "Parque 10": ["306", "640", "815", "501", "402"],
            "Aleixo": ["120", "702", "515", "320"],
            "Cidade Nova": ["640", "815", "306", "435"],
            "Compensa": ["120", "402", "501", "625"],
            "Aeroporto Eduardo Gomes": ["702", "815", "320"]
        }
    
    def abrir_mapa_paradas(self):
        """Abre Google Maps com todas as paradas de ônibus"""
        try:
            # Criar URL do Google Maps com waypoints
            url_base = "https://www.google.com/maps/dir/"
            
            # Adicionar paradas como waypoints (limitar para URL não ficar muito longa)
            waypoints = list(self.paradas_manaus.values())[:8]  # 8 paradas para URL razoável
            
            if waypoints:
                url_waypoints = "/".join(waypoints)
                url_final = f"{url_base}{url_waypoints}"
            else:
                url_final = "https://www.google.com/maps/@-3.1190,-60.0217,12z"
            
            webbrowser.open(url_final)
            return True
            
        except Exception as e:
            print(f"Erro ao abrir mapa: {e}")
            return False
    
    def obter_info_paradas(self):
        """Retorna informações formatadas sobre paradas para mostrar na interface"""
        info_paradas = "📍 PARADAS PRINCIPAIS DE ÔNIBUS - MANAUS:\n\n"
        
        # Agrupar paradas por região
        regioes = {
            "🚌 TERMINAIS": ["Terminal 1 (T1)", "Terminal 2 (T2)", "Terminal 3 (T3)", "Terminal 4 (T4)"],
            "🏛️ CENTRO": ["Praça da Matriz", "Praça da Polícia", "Av. Eduardo Ribeiro", "Porto de Manaus"],
            "🏘️ ZONA SUL": ["Parque 10", "Aleixo", "Coroado", "Japiim"],
            "🏡 ZONA LESTE": ["Cidade Nova", "Novo Aleixo", "Monte das Oliveiras"],
            "🏠 ZONA OESTE": ["Compensa", "Glória", "Vila da Prata"],
            "✈️ PONTOS ESTRATÉGICOS": ["Aeroporto Eduardo Gomes", "Shopping Manaus Via Norte", "Shopping Ponta Negra", "Universidade Federal"]
        }
        
        for regiao, paradas in regioes.items():
            info_paradas += f"{regiao}:\n"
            for parada in paradas:
                if parada in self.linhas_por_parada:
                    linhas = ", ".join(self.linhas_por_parada[parada])
                    info_paradas += f"• {parada}: Linhas {linhas}\n"
            info_paradas += "\n"
        
        return info_paradas
    
    def buscar_paradas_por_linha(self, numero_linha):
        """Busca paradas por número de linha"""
        linhas_paradas = {
            "306": ["Terminal 1 (T1)", "Praça da Matriz", "Parque 10", "Cidade Nova", "Terminal 2 (T2)"],
            "640": ["Terminal 1 (T1)", "Av. Eduardo Ribeiro", "Terminal 3 (T3)", "Cidade Nova"],
            "120": ["Terminal 4 (T4)", "Compensa", "Praça da Polícia", "Terminal 2 (T2)", "Aleixo"],
            "815": ["Terminal 3 (T3)", "Japiim", "Shopping Ponta Negra", "Aeroporto Eduardo Gomes"],
            "402": ["Terminal 4 (T4)", "Compensa", "Praça da Matriz", "Av. Eduardo Ribeiro"],
            "702": ["Aeroporto Eduardo Gomes", "Aleixo", "Shopping Ponta Negra", "Terminal 1 (T1)"],
            "501": ["Terminal 1 (T1)", "Cidade Nova", "Novo Aleixo", "Terminal 3 (T3)"],
            "320": ["Aleixo", "Shopping Ponta Negra", "Av. Eduardo Ribeiro", "Terminal 3 (T3)"]
        }
        
        return linhas_paradas.get(numero_linha, [])
    
    def obter_paradas_proximas(self, localizacao):
        """Retorna paradas próximas a uma localização (para futuras expansões)"""
        # Para implementação com GPS/geolocalização futura
        paradas_ordenadas = []
        # Lógica para ordenar paradas por proximidade...
        return paradas_ordenadas