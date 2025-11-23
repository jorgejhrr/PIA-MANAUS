# 🤝 Guia de Contribuição - PIA Manaus

Obrigado por considerar contribuir com o projeto PIA Manaus! Este documento fornece diretrizes para contribuir com o desenvolvimento do sistema de acessibilidade para transporte público.

## 📋 Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e inclusivo para todos. Esperamos que todos os contribuidores:

- Usem linguagem acolhedora e inclusiva
- Respeitem diferentes pontos de vista e experiências
- Aceitem críticas construtivas de forma profissional
- Foquem no que é melhor para a comunidade
- Demonstrem empatia com outros membros da comunidade

## 🚀 Como Contribuir

### Reportar Bugs

Se você encontrou um bug no sistema, por favor abra uma issue no GitHub incluindo:

**Descrição clara do problema:** Explique o que aconteceu e o que você esperava que acontecesse.

**Passos para reproduzir:** Liste os passos necessários para reproduzir o problema.

**Ambiente:** Inclua informações sobre seu sistema operacional, versão do Python e outras informações relevantes.

**Screenshots ou logs:** Se possível, inclua capturas de tela ou logs de erro que ajudem a entender o problema.

### Sugerir Melhorias

Sugestões de novas funcionalidades ou melhorias são sempre bem-vindas! Ao sugerir uma melhoria, por favor:

- Explique claramente o problema que a funcionalidade resolveria
- Descreva a solução proposta em detalhes
- Considere alternativas e suas vantagens/desvantagens
- Explique como a melhoria beneficiaria os usuários do sistema

### Contribuir com Código

Para contribuir com código, siga estes passos:

#### 1. Fork do Repositório

Faça um fork do repositório PIA-MANAUS para sua conta do GitHub.

#### 2. Clone o Repositório

```bash
git clone https://github.com/SEU_USUARIO/PIA-MANAUS.git
cd PIA-MANAUS
```

#### 3. Crie uma Branch

Crie uma branch para sua feature ou correção:

```bash
git checkout -b feature/minha-nova-feature
```

Ou para correções de bugs:

```bash
git checkout -b fix/correcao-do-bug
```

#### 4. Configure o Ambiente de Desenvolvimento

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 5. Faça suas Alterações

Desenvolva sua feature ou correção seguindo as diretrizes de código abaixo.

#### 6. Execute os Testes

Antes de fazer commit, certifique-se de que todos os testes passam:

```bash
python tests/test_database.py
```

Se você adicionou nova funcionalidade, adicione testes correspondentes.

#### 7. Commit suas Alterações

Faça commits com mensagens claras e descritivas:

```bash
git add .
git commit -m "Adiciona funcionalidade X para melhorar Y"
```

#### 8. Push para o GitHub

```bash
git push origin feature/minha-nova-feature
```

#### 9. Abra um Pull Request

Vá até o repositório original no GitHub e abra um Pull Request da sua branch para a branch principal. Inclua:

- Descrição clara das mudanças
- Referência a issues relacionadas (se houver)
- Screenshots ou GIFs demonstrando a funcionalidade (se aplicável)

## 📝 Diretrizes de Código

### Estilo de Código Python

O projeto segue as convenções PEP 8 para código Python. Principais pontos:

**Indentação:** Use 4 espaços (não tabs)

**Comprimento de linha:** Máximo de 79 caracteres para código, 72 para comentários

**Imports:** Organize imports em três grupos (biblioteca padrão, terceiros, locais), separados por linha em branco

**Nomenclatura:**
- Classes: `PascalCase` (exemplo: `BancoDadosOnibus`)
- Funções e variáveis: `snake_case` (exemplo: `obter_info_linha`)
- Constantes: `UPPER_SNAKE_CASE` (exemplo: `DATABASE_PATH`)

### Documentação

Todas as funções, classes e módulos devem ter docstrings descritivas:

```python
def obter_info_linha(self, numero):
    """
    Obtém informações completas de uma linha específica.
    
    Args:
        numero: Número da linha
        
    Returns:
        Dicionário com informações da linha ou None se não encontrada
    """
    # Implementação
```

### Comentários

Use comentários para explicar **por que** o código faz algo, não **o que** ele faz (o código deve ser autoexplicativo).

### Tratamento de Erros

Sempre trate exceções de forma apropriada e forneça mensagens de erro úteis:

```python
try:
    # Código que pode falhar
    resultado = operacao_arriscada()
except ValueError as e:
    logger.error(f"Erro ao processar: {e}")
    return None
```

### Logging

Use o sistema de logging do projeto em vez de `print()`:

```python
from src.logger import info, error

info("Operação realizada com sucesso")
error("Erro ao processar dados", exc_info=True)
```

## 🧪 Testes

### Escrevendo Testes

Todos os novos recursos devem incluir testes unitários. Coloque os testes no diretório `tests/`:

```python
import unittest
from src.meu_modulo import MinhaClasse

class TestMinhaClasse(unittest.TestCase):
    def setUp(self):
        self.instancia = MinhaClasse()
    
    def test_funcionalidade(self):
        resultado = self.instancia.minha_funcao()
        self.assertEqual(resultado, valor_esperado)
```

### Executando Testes

Execute todos os testes antes de fazer commit:

```bash
python -m unittest discover tests
```

## 📚 Áreas de Contribuição

### Desenvolvimento de Funcionalidades

Algumas áreas onde contribuições são especialmente bem-vindas:

- Expansão do vocabulário de gestos de Libras
- Melhorias na precisão do reconhecimento de voz
- Novos recursos de acessibilidade
- Integração com APIs de transporte público
- Melhorias na interface do usuário

### Documentação

A documentação sempre pode ser melhorada:

- Tradução para outros idiomas
- Tutoriais e guias de uso
- Documentação de API
- Exemplos de código

### Design

Contribuições relacionadas a design são valiosas:

- Melhorias na interface gráfica
- Ícones e recursos visuais
- Temas de cores acessíveis
- Layouts responsivos

### Dados

Ajude a expandir a base de dados:

- Adicionar mais linhas de ônibus de Manaus
- Incluir pontos de parada detalhados
- Atualizar horários e tarifas
- Adicionar informações de acessibilidade

## 🔍 Processo de Revisão

Todos os Pull Requests passam por revisão antes de serem aceitos. Durante a revisão, verificamos:

- Qualidade do código e aderência às diretrizes
- Presença de testes adequados
- Documentação apropriada
- Compatibilidade com o código existente
- Impacto na performance

Esteja preparado para fazer ajustes baseados no feedback da revisão.

## 📞 Dúvidas

Se você tiver dúvidas sobre como contribuir, sinta-se à vontade para:

- Abrir uma issue com a tag "question"
- Entrar em contato através do GitHub
- Consultar a documentação existente

## 🙏 Reconhecimento

Todos os contribuidores serão reconhecidos no projeto. Suas contribuições ajudam a tornar o transporte público mais acessível para todos!

---

**Obrigado por contribuir com o PIA Manaus!** 🚍👐🎤
