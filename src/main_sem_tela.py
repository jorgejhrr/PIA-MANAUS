class PIAManausSistema:
    def __init__(self):
        print("🚀 PIA Manaus - Sistema Inicializado")
    
    def executar_no_console(self):
        print("=" * 50)
        print("🎮 PIA MANAUS - MODO CONSOLE")
        print("=" * 50)
        
        while True:
            print("\n📋 Opções disponíveis:")
            print("1 - Informações de ônibus")
            print("2 - Rotas e direções") 
            print("3 - Pontos próximos")
            print("4 - Sair")
            
            opcao = input("\nEscolha uma opção (1-4): ")
            
            if opcao == "1":
                self.mostrar_info_onibus()
            elif opcao == "2":
                self.mostrar_rotas()
            elif opcao == "3":
                self.mostrar_pontos_proximos()
            elif opcao == "4":
                print("👋 Obrigado por usar o PIA Manaus!")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
    
    def mostrar_info_onibus(self):
        print("\n🚍 LINHAS DE ÔNIBUS DISPONÍVEIS:")
        print("• 640 - Coroado/Alvorada (Terminal 1 → Alvorada)")
        print("• 306 - Cidade Nova/Terminal 3 (Cidade Nova → Terminal 3)")
        print("• 120 - Compensa/Centro (Compensa → Centro)")
        print("• 815 - Jorge Teixeira/Terminal 2 (Jorge Teixeira → Terminal 2)")
        
        linha = input("\nDigite o número da linha para mais informações: ")
        print(f"📊 Buscando informações da linha {line}...")
        print("⏳ Funcionalidade em desenvolvimento!")
    
    def mostrar_rotas(self):
        print("\n🗺️ SISTEMA DE ROTAS:")
        origem = input("Digite a origem (ex: Terminal 1): ")
        destino = input("Digite o destino (ex: Centro): ")
        print(f"📍 Calculando rota de {origem} para {destino}...")
        print("⏳ Integração com Google Maps em desenvolvimento!")
    
    def mostrar_pontos_proximos(self):
        print("\n📍 PONTOS PRÓXIMOS:")
        localizacao = input("Digite sua localização (ex: Terminal 3): ")
        print(f"🔍 Buscando pontos de ônibus próximos a {localizacao}...")
        print("• Terminal 3 - 0.2km")
        print("• Parada Flores - 0.5km") 
        print("• Terminal 2 - 1.2km")

if __name__ == "__main__":
    sistema = PIAManausSistema()
    sistema.executar_no_console()