"""
Testes unitários para o módulo de banco de dados
"""
import unittest
import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database_module_enhanced import BancoDadosOnibusEnhanced


class TestBancoDadosOnibus(unittest.TestCase):
    """Testes para a classe BancoDadosOnibusEnhanced"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração executada uma vez antes de todos os testes"""
        print("\n🧪 Iniciando testes do banco de dados...")
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        # Usar banco em memória para testes
        self.db = BancoDadosOnibusEnhanced(':memory:')
    
    def tearDown(self):
        """Limpeza executada após cada teste"""
        if self.db and self.db.conn:
            self.db.fechar()
    
    def test_criacao_banco(self):
        """Testa se o banco de dados é criado corretamente"""
        self.assertIsNotNone(self.db.conn)
        
        # Verificar se as tabelas foram criadas
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table'
        """)
        tabelas = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('linhas_onibus', tabelas)
        self.assertIn('pontos_parada', tabelas)
        self.assertIn('terminais', tabelas)
    
    def test_obter_info_linha_existente(self):
        """Testa obtenção de informações de linha existente"""
        info = self.db.obter_info_linha('640')
        
        self.assertIsNotNone(info)
        self.assertEqual(info['numero'], '640')
        self.assertEqual(info['nome'], 'Terminal 1 ↔ Terminal 3')
        self.assertTrue(info['acessivel'])
        self.assertTrue(info['ar_condicionado'])
    
    def test_obter_info_linha_inexistente(self):
        """Testa obtenção de informações de linha inexistente"""
        info = self.db.obter_info_linha('999')
        self.assertIsNone(info)
    
    def test_obter_onibus_para_destino(self):
        """Testa busca de ônibus por destino"""
        linhas = self.db.obter_onibus_para_destino('centro')
        
        self.assertIsInstance(linhas, list)
        self.assertGreater(len(linhas), 0)
        
        # Verificar estrutura dos resultados
        for linha in linhas:
            self.assertIn('numero', linha)
            self.assertIn('nome', linha)
            self.assertIn('origem', linha)
            self.assertIn('destino', linha)
    
    def test_obter_linhas_acessiveis(self):
        """Testa obtenção de linhas acessíveis"""
        linhas = self.db.obter_linhas_acessiveis()
        
        self.assertIsInstance(linhas, list)
        self.assertGreater(len(linhas), 0)
        
        # Todas devem ser acessíveis
        for linha in linhas:
            info = self.db.obter_info_linha(linha['numero'])
            self.assertTrue(info['acessivel'])
    
    def test_obter_pontos_parada(self):
        """Testa obtenção de pontos de parada"""
        pontos = self.db.obter_pontos_parada('640')
        
        self.assertIsInstance(pontos, list)
        # Pode estar vazio se não houver pontos cadastrados
        
        if len(pontos) > 0:
            for ponto in pontos:
                self.assertIn('nome', ponto)
                self.assertIn('endereco', ponto)
                self.assertIn('ordem', ponto)
    
    def test_obter_todos_terminais(self):
        """Testa obtenção de todos os terminais"""
        terminais = self.db.obter_todos_terminais()
        
        self.assertIsInstance(terminais, list)
        self.assertGreater(len(terminais), 0)
        
        for terminal in terminais:
            self.assertIn('nome', terminal)
            self.assertIn('endereco', terminal)
            self.assertIn('linhas', terminal)
            self.assertIsInstance(terminal['linhas'], list)
    
    def test_buscar_linhas(self):
        """Testa busca de linhas por termo"""
        # Buscar por número
        linhas = self.db.buscar_linhas('640')
        self.assertGreater(len(linhas), 0)
        self.assertEqual(linhas[0]['numero'], '640')
        
        # Buscar por destino
        linhas = self.db.buscar_linhas('aeroporto')
        self.assertGreater(len(linhas), 0)
        
        # Buscar termo inexistente
        linhas = self.db.buscar_linhas('xyzabc123')
        self.assertEqual(len(linhas), 0)
    
    def test_dados_iniciais_populados(self):
        """Testa se os dados iniciais foram populados"""
        cursor = self.db.conn.cursor()
        
        # Verificar linhas de ônibus
        cursor.execute('SELECT COUNT(*) FROM linhas_onibus')
        count_linhas = cursor.fetchone()[0]
        self.assertGreater(count_linhas, 0)
        
        # Verificar terminais
        cursor.execute('SELECT COUNT(*) FROM terminais')
        count_terminais = cursor.fetchone()[0]
        self.assertGreater(count_terminais, 0)
    
    def test_integridade_dados(self):
        """Testa integridade dos dados"""
        # Todas as linhas devem ter tarifa positiva
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT numero, tarifa FROM linhas_onibus')
        
        for numero, tarifa in cursor.fetchall():
            self.assertGreater(tarifa, 0, 
                f"Linha {numero} tem tarifa inválida: {tarifa}")
    
    def test_compatibilidade_versao_antiga(self):
        """Testa compatibilidade com a versão antiga da API"""
        from database_module_enhanced import BancoDadosOnibus
        
        db_compat = BancoDadosOnibus(':memory:')
        
        # Testar formato antigo de retorno
        info = db_compat.obter_info_linha('640')
        self.assertIsInstance(info, list)
        self.assertEqual(len(info), 5)
        
        # Testar formato antigo de busca por destino
        linhas = db_compat.obter_onibus_para_destino('centro')
        self.assertIsInstance(linhas, list)
        if len(linhas) > 0:
            self.assertIsInstance(linhas[0], list)
            self.assertEqual(len(linhas[0]), 2)
        
        db_compat.fechar()


class TestPerformanceBancoDados(unittest.TestCase):
    """Testes de performance do banco de dados"""
    
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.db = BancoDadosOnibusEnhanced(':memory:')
    
    def tearDown(self):
        """Limpeza executada após cada teste"""
        if self.db and self.db.conn:
            self.db.fechar()
    
    def test_performance_busca_multipla(self):
        """Testa performance de múltiplas buscas"""
        import time
        
        start_time = time.time()
        
        # Realizar 100 buscas
        for i in range(100):
            self.db.obter_info_linha('640')
            self.db.obter_onibus_para_destino('centro')
        
        elapsed_time = time.time() - start_time
        
        # Deve completar em menos de 1 segundo
        self.assertLess(elapsed_time, 1.0,
            f"Buscas muito lentas: {elapsed_time:.2f}s")


def run_tests():
    """Executa todos os testes"""
    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestBancoDadosOnibus))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformanceBancoDados))
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"✅ Sucessos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️  Erros: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
