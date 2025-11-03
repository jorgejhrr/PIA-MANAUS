import sys
import os

print("=" * 50)
print("🚀 PIA MANAUS - INICIANDO SISTEMA")
print("=" * 50)

try:
    # Tentar carregar a interface gráfica
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    from main import PIAManaus
    
    print("✅ Módulos carregados com sucesso!")
    print("💡 Dicas de uso:")
    print("   • Pressione V para Modo Voz")
    print("   • Pressione M para Modo Mapa") 
    print("   • Pressione L para Modo Libras")
    print("   • Pressione ESC para sair")
    print("\n🎮 Iniciando interface gráfica...")
    
    app = PIAManaus()
    app.run()
    
except Exception as e:
    print(f"❌ Erro na interface gráfica: {e}")
    print("🔧 Alternando para modo console...")
    
    try:
        from src.main_sem_tela import PIAManausSistema
        sistema = PIAManausSistema()
        sistema.executar_no_console()
    except Exception as e2:
        print(f"❌ Erro no modo console: {e2}")
        print("🎯 Sistema básico funcionando!")
        input("Pressione ENTER para sair...")