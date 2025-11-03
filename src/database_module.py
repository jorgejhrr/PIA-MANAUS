import sqlite3
import os

class BancoDadosOnibus:
    def __init__(self):
        self.criar_banco_dados()
    
    def criar_banco_dados(self):
        """Cria banco de dados com informações de ônibus de Manaus"""
        try:
            conn = sqlite3.connect(':memory:')  # Banco em memória
            cursor = conn.cursor()
            
            # Criar tabela
            cursor.execute('''
                CREATE TABLE linhas_onibus (
                    numero TEXT PRIMARY KEY,
                    nome TEXT,
                    origem TEXT,
                    destino TEXT,
                    horario TEXT,
                    tarifa REAL
                )
            ''')
            
            # Dados de exemplo para Manaus
            linhas = [
                ('640', 'Terminal 1 ↔ Terminal 3', 'Terminal 1', 'Terminal 3', '05:30-23:00', 4.50),
                ('306', 'Centro ↔ Cidade Nova', 'Centro', 'Cidade Nova', '06:00-22:30', 4.00),
                ('120', 'Aeroporto ↔ Centro', 'Aeroporto', 'Centro', '05:00-24:00', 5.00),
                ('815', 'Coroado ↔ Japiim', 'Coroado', 'Japiim', '06:00-21:00', 3.80),
                ('611', 'Flores ↔ São José', 'Flores', 'São José', '05:45-22:15', 4.20)
            ]
            
            cursor.executemany('''
                INSERT INTO linhas_onibus VALUES (?, ?, ?, ?, ?, ?)
            ''', linhas)
            
            conn.commit()
            self.conn = conn
            print("✅ Banco de dados de ônibus criado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar banco: {e}")
            self.conn = None
    
    def obter_info_linha(self, numero):
        """Obtém informações de uma linha específica"""
        if not self.conn:
            return [numero, f"Linha {numero}", "Terminal", "Centro", "06:00-22:00"]
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT numero, nome, origem, destino, horario 
                FROM linhas_onibus WHERE numero = ?
            ''', (numero,))
            
            resultado = cursor.fetchone()
            if resultado:
                return list(resultado)
            else:
                return [numero, f"Linha {numero} não encontrada", "N/A", "N/A", "N/A"]
                
        except Exception as e:
            print(f"❌ Erro ao buscar linha: {e}")
            return [numero, f"Linha {numero}", "Terminal", "Centro", "06:00-22:00"]
    
    def obter_onibus_para_destino(self, destino):
        """Obtém ônibus que vão para um destino"""
        if not self.conn:
            return [["640", "Linha 640"], ["306", "Linha 306"]]
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT numero, nome FROM linhas_onibus 
                WHERE destino LIKE ? OR origem LIKE ? OR nome LIKE ?
            ''', (f'%{destino}%', f'%{destino}%', f'%{destino}%'))
            
            resultados = cursor.fetchall()
            if resultados:
                return [list(item) for item in resultados]
            else:
                return [["640", f"Ônibus para {destino}"]]
                
        except Exception as e:
            print(f"❌ Erro ao buscar destino: {e}")
            return [["640", "Linha 640"], ["306", "Linha 306"]]

# Fallback
class BancoDadosOnibusFallback:
    def obter_info_linha(self, num): 
        return [num, f"Linha {num}", "Terminal", "Centro", "06:00-22:00"]
    def obter_onibus_para_destino(self, dest): 
        return [[f"640", f"Para {dest}"], ["306", f"Para {dest}"]]