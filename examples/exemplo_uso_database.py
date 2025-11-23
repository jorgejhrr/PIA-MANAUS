"""
Exemplo de uso da API do banco de dados do PIA Manaus

Este script demonstra como usar o módulo de banco de dados
para consultar informações sobre linhas de ônibus.
"""

import sys
import os

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database_module_enhanced import BancoDadosOnibusEnhanced


def exemplo_basico():
    """Exemplo básico de uso do banco de dados"""
    print("=" * 70)
    print("📚 EXEMPLO BÁSICO - Banco de Dados PIA Manaus")
    print("=" * 70)
    print()
    
    # Criar instância do banco de dados
    db = BancoDadosOnibusEnhanced()
    
    # 1. Obter informações de uma linha específica
    print("1️⃣ Consultando informações da linha 640:")
    print("-" * 70)
    
    info = db.obter_info_linha('640')
    if info:
        print(f"   Número: {info['numero']}")
        print(f"   Nome: {info['nome']}")
        print(f"   Origem: {info['origem']}")
        print(f"   Destino: {info['destino']}")
        print(f"   Horário: {info['horario']}")
        print(f"   Tarifa: R$ {info['tarifa']:.2f}")
        print(f"   Acessível: {'Sim' if info['acessivel'] else 'Não'}")
        print(f"   Ar Condicionado: {'Sim' if info['ar_condicionado'] else 'Não'}")
        print(f"   Tipo: {info['tipo']}")
        print(f"   Intervalo: {info['intervalo']} minutos")
    else:
        print("   Linha não encontrada")
    
    print()
    
    # 2. Buscar ônibus para um destino
    print("2️⃣ Buscando ônibus para o Centro:")
    print("-" * 70)
    
    linhas = db.obter_onibus_para_destino('centro')
    for i, linha in enumerate(linhas[:5], 1):
        print(f"   {i}. {linha['numero']} - {linha['nome']}")
        print(f"      De {linha['origem']} para {linha['destino']}")
        print(f"      Tarifa: R$ {linha['tarifa']:.2f} | Tipo: {linha['tipo']}")
        print()
    
    # 3. Listar linhas acessíveis
    print("3️⃣ Linhas com acessibilidade:")
    print("-" * 70)
    
    acessiveis = db.obter_linhas_acessiveis()
    for linha in acessiveis[:5]:
        print(f"   ♿ {linha['numero']} - {linha['nome']}")
    
    print()
    
    # 4. Buscar linhas por termo
    print("4️⃣ Buscando linhas com o termo 'aeroporto':")
    print("-" * 70)
    
    resultados = db.buscar_linhas('aeroporto')
    for linha in resultados:
        print(f"   ✈️  {linha['numero']} - {linha['nome']}")
    
    print()
    
    # 5. Listar terminais
    print("5️⃣ Terminais de ônibus:")
    print("-" * 70)
    
    terminais = db.obter_todos_terminais()
    for terminal in terminais:
        print(f"   🏢 {terminal['nome']}")
        print(f"      Endereço: {terminal['endereco']}")
        print(f"      Linhas: {', '.join(terminal['linhas'])}")
        print()
    
    # Fechar conexão
    db.fechar()
    
    print("=" * 70)
    print("✅ Exemplo concluído!")
    print("=" * 70)


def exemplo_avancado():
    """Exemplo avançado com tratamento de erros"""
    print()
    print("=" * 70)
    print("🚀 EXEMPLO AVANÇADO - Tratamento de Erros e Validação")
    print("=" * 70)
    print()
    
    db = BancoDadosOnibusEnhanced()
    
    # Função auxiliar para validar entrada
    def validar_numero_linha(numero):
        """Valida se o número da linha existe"""
        info = db.obter_info_linha(numero)
        if info:
            return True, info
        return False, None
    
    # Testar várias linhas
    linhas_teste = ['640', '120', '999', 'ABC']
    
    print("🔍 Validando números de linha:")
    print("-" * 70)
    
    for numero in linhas_teste:
        valido, info = validar_numero_linha(numero)
        if valido:
            print(f"   ✅ Linha {numero}: {info['nome']}")
        else:
            print(f"   ❌ Linha {numero}: Não encontrada")
    
    print()
    
    # Buscar com diferentes termos
    termos_busca = ['centro', 'terminal', 'shopping', 'inexistente']
    
    print("🔎 Testando buscas por destino:")
    print("-" * 70)
    
    for termo in termos_busca:
        linhas = db.obter_onibus_para_destino(termo)
        if linhas:
            print(f"   ✅ '{termo}': {len(linhas)} linha(s) encontrada(s)")
        else:
            print(f"   ⚠️  '{termo}': Nenhuma linha encontrada")
    
    print()
    
    # Estatísticas
    print("📊 Estatísticas do banco de dados:")
    print("-" * 70)
    
    cursor = db.conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM linhas_onibus')
    total_linhas = cursor.fetchone()[0]
    print(f"   Total de linhas: {total_linhas}")
    
    cursor.execute('SELECT COUNT(*) FROM linhas_onibus WHERE acessivel = 1')
    linhas_acessiveis = cursor.fetchone()[0]
    print(f"   Linhas acessíveis: {linhas_acessiveis}")
    
    cursor.execute('SELECT COUNT(*) FROM linhas_onibus WHERE ar_condicionado = 1')
    linhas_ar = cursor.fetchone()[0]
    print(f"   Linhas com ar condicionado: {linhas_ar}")
    
    cursor.execute('SELECT AVG(tarifa) FROM linhas_onibus')
    tarifa_media = cursor.fetchone()[0]
    print(f"   Tarifa média: R$ {tarifa_media:.2f}")
    
    cursor.execute('SELECT MIN(tarifa), MAX(tarifa) FROM linhas_onibus')
    tarifa_min, tarifa_max = cursor.fetchone()
    print(f"   Faixa de tarifas: R$ {tarifa_min:.2f} - R$ {tarifa_max:.2f}")
    
    cursor.execute('SELECT COUNT(*) FROM terminais')
    total_terminais = cursor.fetchone()[0]
    print(f"   Total de terminais: {total_terminais}")
    
    db.fechar()
    
    print()
    print("=" * 70)
    print("✅ Exemplo avançado concluído!")
    print("=" * 70)


def exemplo_interativo():
    """Exemplo interativo de consulta"""
    print()
    print("=" * 70)
    print("🎮 EXEMPLO INTERATIVO - Consulta de Linhas")
    print("=" * 70)
    print()
    
    db = BancoDadosOnibusEnhanced()
    
    while True:
        print("\nEscolha uma opção:")
        print("  1. Consultar linha por número")
        print("  2. Buscar ônibus por destino")
        print("  3. Listar linhas acessíveis")
        print("  4. Buscar por termo")
        print("  5. Sair")
        print()
        
        try:
            opcao = input("Opção: ").strip()
            
            if opcao == '1':
                numero = input("Digite o número da linha: ").strip()
                info = db.obter_info_linha(numero)
                if info:
                    print(f"\n✅ Linha {info['numero']} - {info['nome']}")
                    print(f"   De {info['origem']} para {info['destino']}")
                    print(f"   Horário: {info['horario']}")
                    print(f"   Tarifa: R$ {info['tarifa']:.2f}")
                else:
                    print(f"\n❌ Linha {numero} não encontrada")
            
            elif opcao == '2':
                destino = input("Digite o destino: ").strip()
                linhas = db.obter_onibus_para_destino(destino)
                if linhas:
                    print(f"\n✅ Encontradas {len(linhas)} linha(s):")
                    for linha in linhas[:10]:
                        print(f"   {linha['numero']} - {linha['nome']}")
                else:
                    print(f"\n❌ Nenhuma linha encontrada para '{destino}'")
            
            elif opcao == '3':
                linhas = db.obter_linhas_acessiveis()
                print(f"\n✅ {len(linhas)} linhas acessíveis:")
                for linha in linhas:
                    print(f"   ♿ {linha['numero']} - {linha['nome']}")
            
            elif opcao == '4':
                termo = input("Digite o termo de busca: ").strip()
                linhas = db.buscar_linhas(termo)
                if linhas:
                    print(f"\n✅ Encontradas {len(linhas)} linha(s):")
                    for linha in linhas:
                        print(f"   {linha['numero']} - {linha['nome']}")
                else:
                    print(f"\n❌ Nenhuma linha encontrada para '{termo}'")
            
            elif opcao == '5':
                print("\n👋 Até logo!")
                break
            
            else:
                print("\n⚠️  Opção inválida")
        
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    db.fechar()


if __name__ == '__main__':
    # Executar exemplos
    exemplo_basico()
    exemplo_avancado()
    
    # Perguntar se deseja executar o exemplo interativo
    print()
    resposta = input("Deseja executar o exemplo interativo? (s/n): ").strip().lower()
    if resposta == 's':
        exemplo_interativo()
    else:
        print("\n✅ Exemplos concluídos!")
