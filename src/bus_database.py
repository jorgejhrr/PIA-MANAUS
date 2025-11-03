import sqlite3
import os

class BusDatabase:
    def __init__(self, db_path="data/database/bus_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com tabelas e dados de exemplo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de linhas de ônibus
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bus_routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                route_number TEXT UNIQUE NOT NULL,
                route_name TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                schedule TEXT NOT NULL,
                frequency_min INTEGER NOT NULL,
                active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Tabela de interações do usuário
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                system_response TEXT,
                interaction_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN
            )
        ''')
        
        # Inserir dados iniciais
        self.insert_initial_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_initial_data(self, cursor):
        """Insere dados iniciais de exemplo"""
        bus_routes = [
            ('640', 'Coroado/Alvorada', 'Terminal 1', 'Alvorada', '05:00-23:00', 15),
            ('306', 'Cidade Nova/Terminal 3', 'Cidade Nova', 'Terminal 3', '05:30-22:30', 10),
            ('120', 'Compensa/Centro', 'Compensa', 'Centro', '05:15-23:15', 20),
            ('815', 'Jorge Teixeira/Terminal 2', 'Jorge Teixeira', 'Terminal 2', '05:45-22:45', 12),
            ('002', 'Aeroporto/Centro', 'Aeroporto', 'Centro', '04:30-00:00', 30)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO bus_routes 
            (route_number, route_name, origin, destination, schedule, frequency_min)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', bus_routes)
    
    def get_bus_info(self, route_number):
        """Obtém informações de uma linha de ônibus"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT route_number, route_name, origin, destination, schedule, frequency_min
            FROM bus_routes 
            WHERE route_number = ? AND active = TRUE
        ''', (route_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def get_buses_to_destination(self, destination):
        """Obtém ônibus que vão para um destino"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT route_number, route_name
            FROM bus_routes 
            WHERE (destination LIKE ? OR origin LIKE ?) AND active = TRUE
        ''', (f'%{destination}%', f'%{destination}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def log_interaction(self, user_input, system_response, interaction_type, success):
        """Registra interação do usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_interactions 
            (user_input, system_response, interaction_type, success)
            VALUES (?, ?, ?, ?)
        ''', (user_input, system_response, interaction_type, success))
        
        conn.commit()
        conn.close()