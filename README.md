# 🚍 PIA MANAUS - Sistema de Acessibilidade para Transporte Público

**PIA Manaus** é um sistema inovador de informações sobre transporte público desenvolvido especificamente para promover a acessibilidade e inclusão de pessoas com deficiência auditiva e visual na cidade de Manaus. O projeto utiliza tecnologias de inteligência artificial para reconhecimento de voz e Libras (Língua Brasileira de Sinais), proporcionando uma experiência completa e acessível para todos os usuários.

## 🎯 Objetivo

O sistema foi desenvolvido com o objetivo de democratizar o acesso às informações sobre transporte público em Manaus, oferecendo múltiplas formas de interação que atendem às necessidades de diferentes perfis de usuários, especialmente pessoas com deficiência auditiva e visual.

## ✨ Funcionalidades Principais

### 🎤 Reconhecimento de Voz
O sistema permite que usuários façam perguntas por voz sobre linhas de ônibus, horários, destinos e rotas. A tecnologia de reconhecimento de voz processa as perguntas em tempo real e fornece respostas precisas sobre o transporte público de Manaus.

### 👐 Reconhecimento de Libras por Câmera
Utilizando a tecnologia **MediaPipe Hands** do Google, o sistema é capaz de reconhecer gestos de Libras em tempo real através da câmera do computador. Os usuários surdos podem fazer perguntas usando sinais de Libras, e o sistema interpreta esses gestos para fornecer as informações solicitadas.

**Gestos reconhecidos:**
- 🚍 ÔNIBUS (polegar para cima)
- 🏢 TERMINAL (mão aberta)
- ❓ QUAL (indicador para cima)
- ⏰ HORAS (apontar para pulso)
- 📍 CENTRO (apontar para centro)
- 🛫 AEROPORTO (mão plana)
- 📍 ONDE (movimento oscilatório)

### 🗣️ Síntese de Voz (Text-to-Speech)
Todas as respostas do sistema são convertidas em áudio através da tecnologia de síntese de voz, permitindo que pessoas com deficiência visual tenham acesso completo às informações fornecidas pelo sistema.

### 🤖 Avatar em Libras
O sistema conta com um avatar animado que reproduz as respostas em Libras, proporcionando uma comunicação visual completa para usuários surdos. O avatar sincroniza os gestos com o áudio, oferecendo uma experiência multimodal.

### 🗺️ Integração com Google Maps
O sistema permite abrir diretamente o Google Maps com informações sobre Manaus, facilitando a visualização de rotas e localização de pontos de ônibus e terminais.

### 🚌 Banco de Dados de Linhas de Ônibus
O sistema mantém um banco de dados com informações sobre as principais linhas de ônibus de Manaus, incluindo números de linha, nomes, origens, destinos, horários de operação e tarifas.

## 🛠️ Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias e bibliotecas:

| Tecnologia | Versão | Finalidade |
|------------|--------|------------|
| **Python** | 3.11+ | Linguagem principal |
| **Pygame** | 2.5.2 | Interface gráfica e interação |
| **gTTS** | 2.3.2 | Síntese de voz (Text-to-Speech) |
| **SpeechRecognition** | 3.10.0 | Reconhecimento de voz |
| **MediaPipe** | 0.10.0 | Reconhecimento de gestos de Libras |
| **OpenCV** | 4.8.1 | Processamento de imagem da câmera |
| **NumPy** | 1.26.0 | Operações matemáticas e processamento |
| **Pillow** | 10.0.1 | Manipulação de imagens |
| **SQLite3** | - | Banco de dados de linhas de ônibus |

## 📋 Requisitos do Sistema

Para executar o PIA Manaus, seu sistema precisa atender aos seguintes requisitos:

**Sistema Operacional:**
- Windows 10/11
- Linux (Ubuntu 20.04+, Debian, Fedora)
- macOS 10.15+

**Hardware:**
- Processador: Dual-core 2.0 GHz ou superior
- Memória RAM: 4 GB mínimo (8 GB recomendado)
- Webcam: Necessária para reconhecimento de Libras
- Microfone: Necessário para reconhecimento de voz
- Alto-falantes ou fones de ouvido: Para síntese de voz

**Software:**
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Conexão com internet (para síntese de voz e Google Maps)

## 🚀 Instalação

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/jorgejhrr/PIA-MANAUS.git
cd PIA-MANAUS
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
python -m venv venv

# No Windows:
venv\\Scripts\\activate

# No Linux/Mac:
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Executar o Sistema

```bash
python run.py
```

## 📖 Como Usar

### Iniciando o Sistema

Ao executar o comando `python run.py`, o sistema iniciará a interface gráfica com as seguintes opções:

**Atalhos de Teclado:**
- **V** - Ativar modo voz
- **M** - Abrir Google Maps
- **C** - Ativar câmera para Libras
- **L** - Ativar avatar Libras
- **I** - Informações do sistema
- **ESC** - Sair do sistema

### Modo Voz

Pressione **V** ou clique no botão **VOZ** para ativar o reconhecimento de voz. Fale claramente sua pergunta sobre transporte público. Exemplos de perguntas:

- "Qual ônibus vai para o terminal?"
- "Informações do ônibus 640"
- "Que horas chega o ônibus?"
- "Ônibus para o aeroporto"

### Modo Câmera Libras

Pressione **C** ou clique no botão **CÂMERA LIBRAS** para ativar o reconhecimento de gestos. Posicione suas mãos na frente da câmera e faça os gestos de Libras reconhecidos pelo sistema. O sistema detectará os gestos em tempo real e formará perguntas automaticamente.

### Modo Avatar Libras

Pressione **L** ou clique no botão **AVATAR LIBRAS** para visualizar as respostas sendo reproduzidas em Libras pelo avatar animado. Este modo é especialmente útil para usuários surdos que desejam receber as respostas de forma visual.

## 🏗️ Estrutura do Projeto

```
PIA-MANAUS/
├── data/
│   ├── config/
│   │   └── google_maps_api.json
│   └── database/
│       └── onibus_manaus.db
├── src/
│   ├── avatar_libras.py          # Sistema de avatar em Libras
│   ├── bus_database.py            # Gerenciamento do banco de dados
│   ├── camera_libras.py           # Reconhecimento de Libras por câmera
│   ├── database_module.py         # Módulo de banco de dados
│   ├── google_maps_integration.py # Integração com Google Maps
│   ├── libras_model.py            # Modelo de reconhecimento de Libras
│   ├── main.py                    # Interface gráfica principal
│   ├── main_sem_tela.py           # Modo console (fallback)
│   ├── map_renderer.py            # Renderização de mapas
│   ├── multi_language.py          # Suporte multilíngue
│   ├── speech_module.py           # Reconhecimento de voz
│   ├── speech_recognition.py      # Módulo de reconhecimento de fala
│   ├── text_to_speech.py          # Síntese de voz
│   └── text_to_speech_module.py   # Módulo TTS
├── requirements.txt               # Dependências do projeto
├── run.py                         # Script de execução
└── README.md                      # Este arquivo
```

## 🔧 Configuração Avançada

### Banco de Dados

O sistema utiliza SQLite para armazenar informações sobre linhas de ônibus. Por padrão, o banco é criado em memória, mas pode ser configurado para persistência em arquivo editando o arquivo `src/database_module.py`.

### API do Google Maps

Para utilizar recursos avançados do Google Maps, você pode configurar uma chave de API no arquivo `data/config/google_maps_api.json`.

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você deseja contribuir com o projeto PIA Manaus, siga estas etapas:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e de desenvolvimento.

## 👥 Autores

Desenvolvido por **Jorge Junior** ([@jorgejhrr](https://github.com/jorgejhrr))

## 📧 Contato

Para dúvidas, sugestões ou reportar problemas, entre em contato através do GitHub ou abra uma issue no repositório.

## 🙏 Agradecimentos

Agradecimentos especiais às comunidades de desenvolvimento de tecnologias assistivas e aos usuários que contribuíram com feedback para tornar este sistema mais acessível e inclusivo.

---

**PIA Manaus** - Tecnologia a serviço da acessibilidade e inclusão social 🚍👐🎤
