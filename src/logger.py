"""
Sistema de logging para o PIA Manaus
"""
import logging
import os
import sys
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import LOGGING, DATA_DIR
except ImportError:
    # Valores padrão se config não estiver disponível
    LOGGING = {
        'enabled': True,
        'level': 'INFO',
        'file': 'pia_manaus.log',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    }
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


class PIALogger:
    """Classe para gerenciar logging do sistema"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Implementa padrão Singleton"""
        if cls._instance is None:
            cls._instance = super(PIALogger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """Configura o logger"""
        if not LOGGING['enabled']:
            self._logger = logging.getLogger('pia_manaus')
            self._logger.addHandler(logging.NullHandler())
            return
        
        # Criar logger
        self._logger = logging.getLogger('pia_manaus')
        self._logger.setLevel(getattr(logging, LOGGING['level']))
        
        # Evitar duplicação de handlers
        if self._logger.handlers:
            return
        
        # Formato
        formatter = logging.Formatter(LOGGING['format'])
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # Handler para arquivo
        try:
            # Garantir que o diretório existe
            log_dir = os.path.dirname(LOGGING['file'])
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            
            file_handler = logging.FileHandler(
                LOGGING['file'],
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, LOGGING['level']))
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        except Exception as e:
            print(f"⚠️ Não foi possível criar arquivo de log: {e}")
    
    def get_logger(self):
        """Retorna o logger configurado"""
        return self._logger
    
    def debug(self, message):
        """Log de debug"""
        self._logger.debug(message)
    
    def info(self, message):
        """Log de informação"""
        self._logger.info(message)
    
    def warning(self, message):
        """Log de aviso"""
        self._logger.warning(message)
    
    def error(self, message, exc_info=False):
        """Log de erro"""
        self._logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=False):
        """Log crítico"""
        self._logger.critical(message, exc_info=exc_info)
    
    def log_system_start(self):
        """Registra início do sistema"""
        self.info("=" * 60)
        self.info("PIA MANAUS - SISTEMA INICIADO")
        self.info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.info("=" * 60)
    
    def log_system_stop(self):
        """Registra parada do sistema"""
        self.info("=" * 60)
        self.info("PIA MANAUS - SISTEMA ENCERRADO")
        self.info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.info("=" * 60)
    
    def log_module_load(self, module_name, success=True):
        """Registra carregamento de módulo"""
        if success:
            self.info(f"✅ Módulo '{module_name}' carregado com sucesso")
        else:
            self.warning(f"⚠️ Módulo '{module_name}' não pôde ser carregado")
    
    def log_user_action(self, action, details=None):
        """Registra ação do usuário"""
        msg = f"👤 Ação do usuário: {action}"
        if details:
            msg += f" - {details}"
        self.info(msg)
    
    def log_voice_recognition(self, text, success=True):
        """Registra reconhecimento de voz"""
        if success:
            self.info(f"🎤 Voz reconhecida: '{text}'")
        else:
            self.warning(f"🎤 Falha no reconhecimento de voz")
    
    def log_libras_detection(self, gesture):
        """Registra detecção de gesto em Libras"""
        self.info(f"👐 Gesto detectado: '{gesture}'")
    
    def log_database_operation(self, operation, success=True, details=None):
        """Registra operação no banco de dados"""
        status = "✅" if success else "❌"
        msg = f"{status} BD: {operation}"
        if details:
            msg += f" - {details}"
        
        if success:
            self.debug(msg)
        else:
            self.error(msg)
    
    def log_error_with_context(self, error, context=None):
        """Registra erro com contexto"""
        msg = f"❌ ERRO: {str(error)}"
        if context:
            msg += f"\nContexto: {context}"
        self.error(msg, exc_info=True)


# Instância global do logger
_pia_logger = PIALogger()

# Funções de conveniência
def get_logger():
    """Retorna o logger do PIA Manaus"""
    return _pia_logger.get_logger()

def debug(message):
    """Log de debug"""
    _pia_logger.debug(message)

def info(message):
    """Log de informação"""
    _pia_logger.info(message)

def warning(message):
    """Log de aviso"""
    _pia_logger.warning(message)

def error(message, exc_info=False):
    """Log de erro"""
    _pia_logger.error(message, exc_info=exc_info)

def critical(message, exc_info=False):
    """Log crítico"""
    _pia_logger.critical(message, exc_info=exc_info)

def log_system_start():
    """Registra início do sistema"""
    _pia_logger.log_system_start()

def log_system_stop():
    """Registra parada do sistema"""
    _pia_logger.log_system_stop()

def log_module_load(module_name, success=True):
    """Registra carregamento de módulo"""
    _pia_logger.log_module_load(module_name, success)

def log_user_action(action, details=None):
    """Registra ação do usuário"""
    _pia_logger.log_user_action(action, details)

def log_voice_recognition(text, success=True):
    """Registra reconhecimento de voz"""
    _pia_logger.log_voice_recognition(text, success)

def log_libras_detection(gesture):
    """Registra detecção de gesto em Libras"""
    _pia_logger.log_libras_detection(gesture)

def log_database_operation(operation, success=True, details=None):
    """Registra operação no banco de dados"""
    _pia_logger.log_database_operation(operation, success, details)

def log_error_with_context(error, context=None):
    """Registra erro com contexto"""
    _pia_logger.log_error_with_context(error, context)


if __name__ == '__main__':
    # Teste do sistema de logging
    print("🧪 Testando sistema de logging...\n")
    
    log_system_start()
    
    info("Teste de mensagem informativa")
    debug("Teste de mensagem de debug")
    warning("Teste de mensagem de aviso")
    
    log_module_load("speech_recognition", success=True)
    log_module_load("camera_module", success=False)
    
    log_user_action("Ativou modo voz")
    log_voice_recognition("qual ônibus vai para o centro", success=True)
    log_libras_detection("onibus")
    
    log_database_operation("Consulta linha 640", success=True)
    
    try:
        raise ValueError("Erro de teste")
    except Exception as e:
        log_error_with_context(e, context="Teste de erro")
    
    log_system_stop()
    
    print("\n✅ Teste de logging concluído!")
    print(f"📄 Log salvo em: {LOGGING['file']}")
