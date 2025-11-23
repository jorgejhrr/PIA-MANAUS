"""
Arquivo de configuração do PIA Manaus
"""
import os

# Diretórios base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_DIR = os.path.join(DATA_DIR, 'config')
DATABASE_DIR = os.path.join(DATA_DIR, 'database')
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Banco de dados
DATABASE_PATH = os.path.join(DATABASE_DIR, 'onibus_manaus.db')
USE_MEMORY_DB = False  # True para usar banco em memória, False para arquivo

# Interface gráfica
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "PIA Manaus - Sistema de Acessibilidade"
FPS = 60

# Cores (RGB)
COLORS = {
    'background': (0, 51, 102),
    'text': (255, 255, 255),
    'primary': (0, 150, 255),
    'success': (0, 255, 0),
    'warning': (255, 255, 0),
    'error': (255, 0, 0),
    'info': (0, 255, 255),
    'button': (0, 100, 200),
    'button_hover': (0, 150, 255),
    'button_active': (0, 200, 100),
}

# Reconhecimento de voz
SPEECH_RECOGNITION = {
    'timeout': 5,  # segundos
    'phrase_time_limit': 10,  # segundos
    'language': 'pt-BR',
    'energy_threshold': 4000,
}

# Síntese de voz
TEXT_TO_SPEECH = {
    'language': 'pt-BR',
    'slow': False,
    'cache_dir': os.path.join(DATA_DIR, 'tts_cache'),
}

# Reconhecimento de Libras
LIBRAS_RECOGNITION = {
    'camera_index': 0,
    'min_detection_confidence': 0.5,
    'min_tracking_confidence': 0.5,
    'max_num_hands': 2,
    'gesture_hold_time': 2.0,  # segundos
}

# Gestos de Libras reconhecidos
LIBRAS_GESTURES = {
    'onibus': 'Polegar para cima',
    'terminal': 'Mão aberta',
    'qual': 'Indicador para cima',
    'horas': 'Apontar para pulso',
    'centro': 'Apontar para centro',
    'aeroporto': 'Mão plana',
    'onde': 'Movimento oscilatório',
}

# Google Maps
GOOGLE_MAPS = {
    'api_key_file': os.path.join(CONFIG_DIR, 'google_maps_api.json'),
    'default_location': 'Manaus, AM',
    'default_zoom': 12,
}

# Logging
LOGGING = {
    'enabled': True,
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'file': os.path.join(DATA_DIR, 'pia_manaus.log'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}

# Acessibilidade
ACCESSIBILITY = {
    'high_contrast_mode': False,
    'font_size_multiplier': 1.0,
    'screen_reader_support': True,
    'keyboard_shortcuts': True,
}

# Atalhos de teclado
KEYBOARD_SHORTCUTS = {
    'voice_mode': 'v',
    'map_mode': 'm',
    'camera_mode': 'c',
    'libras_mode': 'l',
    'info': 'i',
    'quit': 'escape',
    'help': 'h',
}

# Mensagens do sistema
MESSAGES = {
    'welcome': 'PIA Manaus - Sistema Carregado! Clique em CÂMERA LIBRAS.',
    'voice_listening': '🎤 OUVINDO... FALE AGORA!',
    'voice_processing': '🤔 PROCESSANDO...',
    'voice_error': '❌ Não entendi. Tente novamente.',
    'camera_starting': '📷 INICIANDO CÂMERA COM RECONHECIMENTO DE LIBRAS...',
    'camera_active': '📷 CÂMERA ATIVA - FAÇA GESTOS DE LIBRAS!',
    'camera_error': '❌ Erro ao iniciar câmera',
    'libras_detected': '👐 GESTO DETECTADO: {}',
    'response_ready': '💡 RESPOSTA PRONTA!',
    'map_opening': '🗺️ Abrindo Google Maps...',
    'map_opened': '🗺️ Google Maps aberto!',
}

# Informações do sistema
SYSTEM_INFO = {
    'name': 'PIA Manaus',
    'version': '2.0.0',
    'description': 'Sistema de Acessibilidade para Transporte Público',
    'author': 'Jorge Junior',
    'github': 'https://github.com/jorgejhrr/PIA-MANAUS',
}

# Criar diretórios necessários
def criar_diretorios():
    """Cria diretórios necessários se não existirem"""
    dirs = [DATA_DIR, CONFIG_DIR, DATABASE_DIR]
    
    if TEXT_TO_SPEECH['cache_dir']:
        dirs.append(TEXT_TO_SPEECH['cache_dir'])
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)


if __name__ == '__main__':
    print("📋 Configurações do PIA Manaus")
    print(f"Versão: {SYSTEM_INFO['version']}")
    print(f"Banco de dados: {DATABASE_PATH}")
    print(f"Diretório de dados: {DATA_DIR}")
    
    criar_diretorios()
    print("\n✅ Diretórios criados com sucesso!")
