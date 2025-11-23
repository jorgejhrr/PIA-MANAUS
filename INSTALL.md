# 📦 Guia de Instalação - PIA Manaus

Este documento fornece instruções detalhadas para instalar e configurar o sistema PIA Manaus em diferentes sistemas operacionais.

## 📋 Índice

- [Requisitos do Sistema](#requisitos-do-sistema)
- [Instalação no Windows](#instalação-no-windows)
- [Instalação no Linux](#instalação-no-linux)
- [Instalação no macOS](#instalação-no-macos)
- [Configuração Avançada](#configuração-avançada)
- [Solução de Problemas](#solução-de-problemas)

## 🖥️ Requisitos do Sistema

### Hardware Mínimo

O sistema PIA Manaus requer as seguintes especificações mínimas de hardware para funcionar adequadamente:

**Processador:** Dual-core 2.0 GHz ou superior (recomendado: Quad-core 2.5 GHz)

**Memória RAM:** 4 GB mínimo (recomendado: 8 GB ou mais)

**Espaço em Disco:** 500 MB livres para instalação e dados

**Webcam:** Necessária para o recurso de reconhecimento de Libras (resolução mínima 720p)

**Microfone:** Necessário para o recurso de reconhecimento de voz

**Alto-falantes/Fones:** Necessários para a síntese de voz

### Software Necessário

**Python:** Versão 3.11 ou superior é obrigatória

**pip:** Gerenciador de pacotes Python (geralmente incluído com Python)

**Git:** Para clonar o repositório (opcional, mas recomendado)

**Conexão com Internet:** Necessária para síntese de voz e integração com Google Maps

## 🪟 Instalação no Windows

### Passo 1: Instalar Python

Acesse o site oficial do Python em [python.org](https://www.python.org/downloads/) e baixe a versão mais recente do Python 3.11 ou superior para Windows. Durante a instalação, certifique-se de marcar a opção **"Add Python to PATH"** para facilitar o uso do Python no terminal.

Após a instalação, abra o Prompt de Comando (cmd) e verifique se o Python foi instalado corretamente executando o comando:

```cmd
python --version
```

O comando deve retornar a versão do Python instalada, por exemplo: `Python 3.11.0`.

### Passo 2: Instalar Git (Opcional)

Se você deseja clonar o repositório usando Git, baixe e instale o Git para Windows em [git-scm.com](https://git-scm.com/download/win). Após a instalação, você poderá usar o Git Bash ou o Prompt de Comando para executar comandos Git.

### Passo 3: Clonar o Repositório

Abra o Prompt de Comando ou Git Bash e navegue até o diretório onde deseja instalar o PIA Manaus. Execute o seguinte comando para clonar o repositório:

```cmd
git clone https://github.com/jorgejhrr/PIA-MANAUS.git
cd PIA-MANAUS
```

Se você não tem o Git instalado, pode baixar o repositório como arquivo ZIP diretamente do GitHub e extraí-lo em um diretório de sua escolha.

### Passo 4: Criar Ambiente Virtual

É altamente recomendado criar um ambiente virtual Python para isolar as dependências do projeto. No diretório do projeto, execute:

```cmd
python -m venv venv
```

Para ativar o ambiente virtual no Windows, execute:

```cmd
venv\Scripts\activate
```

Após a ativação, você verá `(venv)` no início da linha de comando, indicando que o ambiente virtual está ativo.

### Passo 5: Instalar Dependências

Com o ambiente virtual ativado, instale todas as dependências do projeto executando:

```cmd
pip install -r requirements.txt
```

Este comando instalará todas as bibliotecas necessárias, incluindo Pygame, gTTS, SpeechRecognition, MediaPipe, OpenCV e outras.

### Passo 6: Executar o Sistema

Após a instalação das dependências, você pode executar o sistema com o comando:

```cmd
python run.py
```

O sistema iniciará a interface gráfica e estará pronto para uso.

## 🐧 Instalação no Linux

### Passo 1: Instalar Python

A maioria das distribuições Linux já vem com Python instalado. Verifique a versão instalada com:

```bash
python3 --version
```

Se a versão for inferior a 3.11, você precisará instalar uma versão mais recente. No Ubuntu/Debian, execute:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

No Fedora, execute:

```bash
sudo dnf install python3.11 python3-pip
```

### Passo 2: Instalar Dependências do Sistema

Algumas bibliotecas Python requerem pacotes do sistema. Instale-os com:

**Ubuntu/Debian:**
```bash
sudo apt install python3-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt install ffmpeg libsm6 libxext6 libxrender-dev
```

**Fedora:**
```bash
sudo dnf install python3-devel portaudio-devel
sudo dnf install ffmpeg libSM libXext libXrender
```

### Passo 3: Clonar o Repositório

```bash
git clone https://github.com/jorgejhrr/PIA-MANAUS.git
cd PIA-MANAUS
```

### Passo 4: Criar Ambiente Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Passo 5: Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### Passo 6: Configurar Permissões de Câmera e Microfone

Certifique-se de que seu usuário tem permissões para acessar a câmera e o microfone. Você pode precisar adicionar seu usuário aos grupos apropriados:

```bash
sudo usermod -a -G video $USER
sudo usermod -a -G audio $USER
```

Após executar esses comandos, faça logout e login novamente para que as mudanças tenham efeito.

### Passo 7: Executar o Sistema

```bash
python run.py
```

## 🍎 Instalação no macOS

### Passo 1: Instalar Homebrew

Se você ainda não tem o Homebrew instalado, abra o Terminal e execute:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Passo 2: Instalar Python

```bash
brew install python@3.11
```

### Passo 3: Instalar Dependências do Sistema

```bash
brew install portaudio ffmpeg
```

### Passo 4: Clonar o Repositório

```bash
git clone https://github.com/jorgejhrr/PIA-MANAUS.git
cd PIA-MANAUS
```

### Passo 5: Criar Ambiente Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Passo 6: Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### Passo 7: Configurar Permissões

O macOS pode solicitar permissões para acessar a câmera e o microfone quando você executar o sistema pela primeira vez. Certifique-se de conceder essas permissões nas Preferências do Sistema.

### Passo 8: Executar o Sistema

```bash
python run.py
```

## ⚙️ Configuração Avançada

### Configurar Banco de Dados Persistente

Por padrão, o sistema pode usar um banco de dados em memória. Para usar persistência em arquivo, edite o arquivo `config.py` e configure:

```python
USE_MEMORY_DB = False
DATABASE_PATH = os.path.join(DATABASE_DIR, 'onibus_manaus.db')
```

### Configurar API do Google Maps

Para recursos avançados do Google Maps, você pode configurar uma chave de API. Crie um arquivo `data/config/google_maps_api.json` com o seguinte conteúdo:

```json
{
  "api_key": "SUA_CHAVE_API_AQUI"
}
```

Obtenha uma chave de API em [Google Cloud Console](https://console.cloud.google.com/).

### Ajustar Configurações de Reconhecimento de Voz

Edite o arquivo `config.py` para ajustar parâmetros de reconhecimento de voz:

```python
SPEECH_RECOGNITION = {
    'timeout': 5,
    'phrase_time_limit': 10,
    'language': 'pt-BR',
    'energy_threshold': 4000,
}
```

### Configurar Logging

Para habilitar ou ajustar o sistema de logging, edite `config.py`:

```python
LOGGING = {
    'enabled': True,
    'level': 'INFO',
    'file': os.path.join(DATA_DIR, 'pia_manaus.log'),
}
```

## 🔧 Solução de Problemas

### Erro: "ModuleNotFoundError: No module named 'pygame'"

**Solução:** Certifique-se de que o ambiente virtual está ativado e execute `pip install -r requirements.txt` novamente.

### Erro: "Câmera não disponível"

**Solução:** Verifique se sua câmera está conectada e funcionando. No Linux, verifique as permissões com `ls -l /dev/video*`. No Windows/macOS, verifique as configurações de privacidade do sistema.

### Erro: "Microfone não detectado"

**Solução:** Verifique se o microfone está conectado e configurado como dispositivo padrão nas configurações de áudio do sistema. No Linux, você pode precisar instalar `pulseaudio` ou `alsa-utils`.

### Erro: "ImportError: libportaudio.so.2"

**Solução (Linux):** Instale a biblioteca PortAudio com `sudo apt install portaudio19-dev libportaudio2` (Ubuntu/Debian) ou `sudo dnf install portaudio-devel` (Fedora).

### Síntese de Voz não funciona

**Solução:** A síntese de voz (gTTS) requer conexão com a internet. Verifique sua conexão e certifique-se de que não há bloqueios de firewall.

### Performance lenta no reconhecimento de Libras

**Solução:** O reconhecimento de Libras usa MediaPipe, que pode ser intensivo em CPU. Certifique-se de que seu computador atende aos requisitos mínimos. Você pode ajustar os parâmetros de detecção em `config.py` para melhorar a performance.

### Erro: "sqlite3.OperationalError: database is locked"

**Solução:** Certifique-se de que apenas uma instância do sistema está rodando. Se o problema persistir, delete o arquivo `data/database/onibus_manaus.db` e reinicie o sistema.

## 📞 Suporte

Se você encontrar problemas não listados aqui, por favor:

1. Verifique as [Issues do GitHub](https://github.com/jorgejhrr/PIA-MANAUS/issues)
2. Crie uma nova issue com detalhes do problema
3. Inclua informações sobre seu sistema operacional e versão do Python

---

**PIA Manaus** - Acessibilidade para todos 🚍👐🎤
