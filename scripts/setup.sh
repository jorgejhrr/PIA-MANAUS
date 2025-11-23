#!/bin/bash
# Script de instalação automatizada do PIA Manaus

set -e  # Parar em caso de erro

echo "=================================================="
echo "🚍 PIA MANAUS - Script de Instalação Automatizada"
echo "=================================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "ℹ️  $1"
}

# Verificar sistema operacional
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    print_info "Sistema operacional detectado: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
    print_info "Sistema operacional detectado: macOS"
else
    print_warning "Sistema operacional não reconhecido: $OSTYPE"
fi

# Verificar Python
echo ""
print_info "Verificando instalação do Python..."

if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    print_success "Python 3.11 encontrado"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_CMD="python3"
    print_success "Python $PYTHON_VERSION encontrado"
else
    print_error "Python 3 não encontrado!"
    print_info "Por favor, instale Python 3.11 ou superior"
    exit 1
fi

# Verificar versão do Python
PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
    print_warning "Python $PYTHON_VERSION detectado. Recomendado: 3.11+"
else
    print_success "Versão do Python adequada: $PYTHON_VERSION"
fi

# Verificar pip
echo ""
print_info "Verificando pip..."

if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    print_success "pip encontrado"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    print_success "pip encontrado"
else
    print_error "pip não encontrado!"
    exit 1
fi

# Instalar dependências do sistema (Linux)
if [ "$OS" == "linux" ]; then
    echo ""
    print_info "Verificando dependências do sistema..."
    
    if command -v apt-get &> /dev/null; then
        print_info "Detectado sistema baseado em Debian/Ubuntu"
        print_warning "Algumas dependências podem requerer sudo"
        
        read -p "Deseja instalar dependências do sistema? (s/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            sudo apt-get update
            sudo apt-get install -y python3-dev portaudio19-dev libportaudio2
            sudo apt-get install -y ffmpeg libsm6 libxext6 libxrender-dev
            print_success "Dependências do sistema instaladas"
        fi
    elif command -v dnf &> /dev/null; then
        print_info "Detectado sistema baseado em Fedora"
        print_warning "Algumas dependências podem requerer sudo"
        
        read -p "Deseja instalar dependências do sistema? (s/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            sudo dnf install -y python3-devel portaudio-devel
            sudo dnf install -y ffmpeg libSM libXext libXrender
            print_success "Dependências do sistema instaladas"
        fi
    fi
fi

# Criar ambiente virtual
echo ""
print_info "Criando ambiente virtual..."

if [ -d "venv" ]; then
    print_warning "Ambiente virtual já existe"
    read -p "Deseja recriar o ambiente virtual? (s/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf venv
        $PYTHON_CMD -m venv venv
        print_success "Ambiente virtual recriado"
    fi
else
    $PYTHON_CMD -m venv venv
    print_success "Ambiente virtual criado"
fi

# Ativar ambiente virtual
print_info "Ativando ambiente virtual..."
source venv/bin/activate
print_success "Ambiente virtual ativado"

# Atualizar pip
echo ""
print_info "Atualizando pip..."
$PIP_CMD install --upgrade pip
print_success "pip atualizado"

# Instalar dependências Python
echo ""
print_info "Instalando dependências Python..."
$PIP_CMD install -r requirements.txt
print_success "Dependências Python instaladas"

# Criar diretórios necessários
echo ""
print_info "Criando estrutura de diretórios..."
mkdir -p data/config data/database data/tts_cache
print_success "Diretórios criados"

# Inicializar banco de dados
echo ""
print_info "Inicializando banco de dados..."
$PYTHON_CMD src/database_module_enhanced.py > /dev/null 2>&1
print_success "Banco de dados inicializado"

# Verificar instalação
echo ""
print_info "Verificando instalação..."

# Testar imports
$PYTHON_CMD -c "import pygame; import gtts; import speech_recognition; import mediapipe; import cv2" 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Todas as bibliotecas foram instaladas corretamente"
else
    print_error "Algumas bibliotecas não foram instaladas corretamente"
    exit 1
fi

# Executar testes
echo ""
print_info "Executando testes..."
$PYTHON_CMD tests/test_database.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_success "Todos os testes passaram"
else
    print_warning "Alguns testes falharam (não crítico)"
fi

# Resumo
echo ""
echo "=================================================="
echo "✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=================================================="
echo ""
echo "Para executar o PIA Manaus:"
echo "  1. Ative o ambiente virtual:"
echo "     source venv/bin/activate"
echo "  2. Execute o sistema:"
echo "     python run.py"
echo ""
echo "Para mais informações, consulte:"
echo "  - README.md"
echo "  - INSTALL.md"
echo ""
echo "=================================================="
