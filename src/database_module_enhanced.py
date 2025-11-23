import sqlite3
import os

class BancoDadosOnibusEnhanced:
    """
    Banco de dados aprimorado para o sistema PIA Manaus.
    Inclui mais linhas de ônibus, pontos de parada e informações de acessibilidade.
    """
    
    def __init__(self, db_path=None):
        """
        Inicializa o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados. 
                    Se None, usa banco em memória.
        """
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 'data', 'database', 'onibus_manaus.db'
            )
        
        self.db_path = db_path
        self.conn = None
        self.criar_banco_dados()
    
    def criar_banco_dados(self):
        """Cria banco de dados com estrutura completa"""
        try:
            # Criar diretório se não existir
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
            
            # Criar tabela de linhas de ônibus
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS linhas_onibus (
                    numero TEXT PRIMARY KEY,
                    nome TEXT NOT NULL,
                    origem TEXT NOT NULL,
                    destino TEXT NOT NULL,
                    horario_inicio TEXT,
                    horario_fim TEXT,
                    intervalo_minutos INTEGER,
                    tarifa REAL,
                    acessivel BOOLEAN,
                    ar_condicionado BOOLEAN,
                    tipo TEXT
                )
            ''')
            
            # Criar tabela de pontos de parada
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pontos_parada (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    linha_numero TEXT,
                    nome_ponto TEXT,
                    endereco TEXT,
                    latitude REAL,
                    longitude REAL,
                    ordem INTEGER,
                    FOREIGN KEY (linha_numero) REFERENCES linhas_onibus(numero)
                )
            ''')
            
            # Criar tabela de terminais
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS terminais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    endereco TEXT,
                    latitude REAL,
                    longitude REAL,
                    linhas_atendidas TEXT
                )
            ''')
            
            # Verificar se já existem dados
            cursor.execute('SELECT COUNT(*) FROM linhas_onibus')
            if cursor.fetchone()[0] == 0:
                self.popular_dados_iniciais(cursor)
            
            self.conn.commit()
            print("✅ Banco de dados aprimorado criado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao criar banco: {e}")
            self.conn = None
    
    def popular_dados_iniciais(self, cursor):
        """Popula o banco com dados iniciais de Manaus"""
        
        # Linhas de ônibus expandidas (baseadas em linhas reais de Manaus)
        linhas = [
            # Formato: (numero, nome, origem, destino, hr_inicio, hr_fim, intervalo, tarifa, acessivel, ar_cond, tipo)
            ('010', 'Terminal 1 ↔ Centro', 'Terminal 1', 'Centro', '05:00', '23:30', 15, 4.50, True, True, 'Executivo'),
            ('120', 'Aeroporto ↔ Centro', 'Aeroporto Eduardo Gomes', 'Centro', '05:00', '00:00', 20, 5.00, True, True, 'Executivo'),
            ('201', 'Cidade Nova ↔ Centro', 'Cidade Nova', 'Centro', '05:30', '23:00', 12, 4.00, True, False, 'Convencional'),
            ('306', 'Centro ↔ Aleixo', 'Centro', 'Aleixo', '06:00', '22:30', 18, 4.00, True, False, 'Convencional'),
            ('418', 'Flores ↔ Centro', 'Flores', 'Centro', '05:45', '22:45', 15, 4.20, True, False, 'Convencional'),
            ('510', 'São José ↔ Terminal 2', 'São José', 'Terminal 2', '05:30', '23:00', 20, 4.00, False, False, 'Convencional'),
            ('611', 'Flores ↔ São José', 'Flores', 'São José', '05:45', '22:15', 25, 4.20, True, False, 'Convencional'),
            ('640', 'Terminal 1 ↔ Terminal 3', 'Terminal 1', 'Terminal 3', '05:30', '23:00', 10, 4.50, True, True, 'Executivo'),
            ('750', 'Japiim ↔ Centro', 'Japiim', 'Centro', '06:00', '22:00', 20, 4.00, False, False, 'Convencional'),
            ('815', 'Coroado ↔ Japiim', 'Coroado', 'Japiim', '06:00', '21:00', 30, 3.80, False, False, 'Convencional'),
            ('A001', 'Circular Terminal 1', 'Terminal 1', 'Terminal 1', '05:00', '23:30', 8, 4.00, True, False, 'Circular'),
            ('A002', 'Circular Terminal 2', 'Terminal 2', 'Terminal 2', '05:00', '23:30', 8, 4.00, True, False, 'Circular'),
            ('A003', 'Circular Terminal 3', 'Terminal 3', 'Terminal 3', '05:00', '23:30', 8, 4.00, True, False, 'Circular'),
            ('300', 'Compensa ↔ Centro', 'Compensa', 'Centro', '05:30', '22:30', 15, 4.00, True, False, 'Convencional'),
            ('455', 'Alvorada ↔ Terminal 1', 'Alvorada', 'Terminal 1', '05:45', '22:45', 20, 4.20, False, False, 'Convencional'),
            ('520', 'Colônia Terra Nova ↔ Centro', 'Colônia Terra Nova', 'Centro', '06:00', '21:30', 25, 4.00, False, False, 'Convencional'),
            ('670', 'Novo Israel ↔ Terminal 2', 'Novo Israel', 'Terminal 2', '05:30', '22:00', 22, 4.00, True, False, 'Convencional'),
            ('701', 'Tarumã ↔ Centro', 'Tarumã', 'Centro', '06:00', '22:00', 18, 4.20, False, False, 'Convencional'),
            ('800', 'Ponta Negra ↔ Centro', 'Ponta Negra', 'Centro', '05:30', '23:00', 15, 4.50, True, True, 'Executivo'),
            ('900', 'Shopping Manauara ↔ Centro', 'Shopping Manauara', 'Centro', '06:00', '22:30', 12, 4.50, True, True, 'Executivo'),
        ]
        
        cursor.executemany('''
            INSERT INTO linhas_onibus VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', linhas)
        
        # Terminais
        terminais = [
            ('Terminal 1 - T1', 'Av. Constantino Nery', -3.0952, -60.0217, '010,640,455,A001'),
            ('Terminal 2 - T2', 'Av. Autaz Mirim', -3.1190, -59.9843, '510,670,A002'),
            ('Terminal 3 - T3', 'Av. Grande Circular', -3.0744, -60.0589, '640,A003'),
            ('Terminal 4 - T4', 'Av. Brasil', -3.1089, -60.0250, '201,300'),
        ]
        
        cursor.executemany('''
            INSERT INTO terminais (nome, endereco, latitude, longitude, linhas_atendidas)
            VALUES (?, ?, ?, ?, ?)
        ''', terminais)
        
        # Pontos de parada de exemplo para algumas linhas
        pontos = [
            ('640', 'Terminal 1', 'Av. Constantino Nery', -3.0952, -60.0217, 1),
            ('640', 'Shopping Manauara', 'Av. Mário Ypiranga', -3.0889, -60.0583, 2),
            ('640', 'Praça 14', 'Av. 7 de Setembro', -3.1319, -60.0217, 3),
            ('640', 'Terminal 3', 'Av. Grande Circular', -3.0744, -60.0589, 4),
            ('120', 'Aeroporto', 'Av. Santos Dumont', -3.0386, -60.0497, 1),
            ('120', 'Ponta Negra', 'Av. do Turismo', -3.0697, -60.0925, 2),
            ('120', 'Centro', 'Av. Eduardo Ribeiro', -3.1319, -60.0217, 3),
        ]
        
        cursor.executemany('''
            INSERT INTO pontos_parada (linha_numero, nome_ponto, endereco, latitude, longitude, ordem)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', pontos)
    
    def obter_info_linha(self, numero):
        """
        Obtém informações completas de uma linha específica.
        
        Args:
            numero: Número da linha
            
        Returns:
            Lista com informações da linha ou None se não encontrada
        """
        if not self.conn:
            return None
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT numero, nome, origem, destino, 
                       horario_inicio || '-' || horario_fim as horario,
                       tarifa, acessivel, ar_condicionado, tipo, intervalo_minutos
                FROM linhas_onibus 
                WHERE numero = ?
            ''', (numero,))
            
            resultado = cursor.fetchone()
            if resultado:
                return {
                    'numero': resultado[0],
                    'nome': resultado[1],
                    'origem': resultado[2],
                    'destino': resultado[3],
                    'horario': resultado[4],
                    'tarifa': resultado[5],
                    'acessivel': bool(resultado[6]),
                    'ar_condicionado': bool(resultado[7]),
                    'tipo': resultado[8],
                    'intervalo': resultado[9]
                }
            return None
                
        except Exception as e:
            print(f"❌ Erro ao buscar linha: {e}")
            return None
    
    def obter_onibus_para_destino(self, destino):
        """
        Obtém ônibus que vão para um destino específico.
        
        Args:
            destino: Nome do destino
            
        Returns:
            Lista de dicionários com informações das linhas
        """
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT numero, nome, origem, destino, tarifa, acessivel, tipo
                FROM linhas_onibus 
                WHERE LOWER(destino) LIKE ? 
                   OR LOWER(origem) LIKE ? 
                   OR LOWER(nome) LIKE ?
                ORDER BY numero
            ''', (f'%{destino.lower()}%', f'%{destino.lower()}%', f'%{destino.lower()}%'))
            
            resultados = cursor.fetchall()
            return [
                {
                    'numero': r[0],
                    'nome': r[1],
                    'origem': r[2],
                    'destino': r[3],
                    'tarifa': r[4],
                    'acessivel': bool(r[5]),
                    'tipo': r[6]
                }
                for r in resultados
            ]
                
        except Exception as e:
            print(f"❌ Erro ao buscar destino: {e}")
            return []
    
    def obter_linhas_acessiveis(self):
        """Retorna todas as linhas com acessibilidade"""
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT numero, nome, origem, destino
                FROM linhas_onibus 
                WHERE acessivel = 1
                ORDER BY numero
            ''')
            
            return [
                {'numero': r[0], 'nome': r[1], 'origem': r[2], 'destino': r[3]}
                for r in cursor.fetchall()
            ]
        except Exception as e:
            print(f"❌ Erro ao buscar linhas acessíveis: {e}")
            return []
    
    def obter_pontos_parada(self, linha_numero):
        """Retorna os pontos de parada de uma linha"""
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT nome_ponto, endereco, latitude, longitude, ordem
                FROM pontos_parada
                WHERE linha_numero = ?
                ORDER BY ordem
            ''', (linha_numero,))
            
            return [
                {
                    'nome': r[0],
                    'endereco': r[1],
                    'latitude': r[2],
                    'longitude': r[3],
                    'ordem': r[4]
                }
                for r in cursor.fetchall()
            ]
        except Exception as e:
            print(f"❌ Erro ao buscar pontos de parada: {e}")
            return []
    
    def obter_todos_terminais(self):
        """Retorna informações de todos os terminais"""
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT nome, endereco, latitude, longitude, linhas_atendidas
                FROM terminais
                ORDER BY nome
            ''')
            
            return [
                {
                    'nome': r[0],
                    'endereco': r[1],
                    'latitude': r[2],
                    'longitude': r[3],
                    'linhas': r[4].split(',') if r[4] else []
                }
                for r in cursor.fetchall()
            ]
        except Exception as e:
            print(f"❌ Erro ao buscar terminais: {e}")
            return []
    
    def buscar_linhas(self, termo):
        """
        Busca linhas por termo (número, nome, origem ou destino).
        
        Args:
            termo: Termo de busca
            
        Returns:
            Lista de dicionários com informações das linhas
        """
        if not self.conn:
            return []
            
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT numero, nome, origem, destino, tarifa, tipo
                FROM linhas_onibus 
                WHERE LOWER(numero) LIKE ? 
                   OR LOWER(nome) LIKE ?
                   OR LOWER(origem) LIKE ?
                   OR LOWER(destino) LIKE ?
                ORDER BY numero
            ''', tuple([f'%{termo.lower()}%'] * 4))
            
            return [
                {
                    'numero': r[0],
                    'nome': r[1],
                    'origem': r[2],
                    'destino': r[3],
                    'tarifa': r[4],
                    'tipo': r[5]
                }
                for r in cursor.fetchall()
            ]
        except Exception as e:
            print(f"❌ Erro ao buscar linhas: {e}")
            return []
    
    def fechar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("✅ Conexão com banco de dados fechada")


# Manter compatibilidade com código antigo
class BancoDadosOnibus(BancoDadosOnibusEnhanced):
    """Classe de compatibilidade com a versão antiga"""
    
    def obter_info_linha(self, numero):
        """Retorna no formato antigo para compatibilidade"""
        info = super().obter_info_linha(numero)
        if info:
            return [
                info['numero'],
                info['nome'],
                info['origem'],
                info['destino'],
                info['horario']
            ]
        return [numero, f"Linha {numero} não encontrada", "N/A", "N/A", "N/A"]
    
    def obter_onibus_para_destino(self, destino):
        """Retorna no formato antigo para compatibilidade"""
        linhas = super().obter_onibus_para_destino(destino)
        return [[linha['numero'], linha['nome']] for linha in linhas]


if __name__ == "__main__":
    # Teste do banco de dados
    print("🧪 Testando banco de dados aprimorado...")
    
    db = BancoDadosOnibusEnhanced()
    
    print("\n📊 Informações da linha 640:")
    info = db.obter_info_linha('640')
    if info:
        for chave, valor in info.items():
            print(f"  {chave}: {valor}")
    
    print("\n🔍 Ônibus para o Centro:")
    linhas = db.obter_onibus_para_destino('centro')
    for linha in linhas[:5]:
        print(f"  {linha['numero']} - {linha['nome']}")
    
    print("\n♿ Linhas acessíveis:")
    acessiveis = db.obter_linhas_acessiveis()
    for linha in acessiveis[:5]:
        print(f"  {linha['numero']} - {linha['nome']}")
    
    print("\n🏢 Terminais:")
    terminais = db.obter_todos_terminais()
    for terminal in terminais:
        print(f"  {terminal['nome']} - {len(terminal['linhas'])} linhas")
    
    db.fechar()
    print("\n✅ Teste concluído!")
