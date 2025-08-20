# 🚀 FiveM Escrow Decryptor - Sistema Automático v2.0

## 📋 Descrição

O **FiveM Escrow Decryptor** é uma ferramenta avançada desenvolvida para decriptar arquivos protegidos pelo sistema de escrow da FiveM. Este sistema automatiza todo o processo de decriptação, desde a validação de chaves de servidor até a extração completa dos recursos protegidos.

## ✨ Características Principais

- 🔐 **Validação Automática de Chaves**: Verifica automaticamente a validade das Server Keys da FiveM
- 🚀 **Decriptação em Lote**: Processa múltiplos arquivos simultaneamente
- 📊 **Interface Visual**: Interface colorida e intuitiva com barras de progresso
- 💾 **Sistema de Cache**: Armazena chaves para otimizar o processo
- 🎯 **Suporte a Múltiplos Recursos**: Processa todos os recursos disponíveis na Server Key
- 🔄 **Processamento Paralelo**: Utiliza threads para melhor performance
- 📁 **Organização Automática**: Cria estrutura de pastas organizada

## 🛠️ Requisitos do Sistema

- **Python 3.7+** instalado no sistema
- **Windows 10/11** (testado e otimizado)
- **Conexão com a internet** para validação de chaves
- **Server Key válida** da FiveM

## 📦 Dependências

O sistema requer as seguintes bibliotecas Python:

- `requests` - Para comunicação HTTP com a API da FiveM
- `colorama` - Para interface colorida no terminal
- `pycryptodome` - Para algoritmos de criptografia
- `tqdm` - Para barras de progresso

## 🚀 Instalação

### Método 1: Instalador Automático (Recomendado)

1. Execute o arquivo `instalador.bat` como administrador
2. Aguarde a instalação automática das dependências
3. Pronto! Todas as dependências serão instaladas automaticamente

### Método 2: Instalação Manual

```bash
pip install requests colorama pycryptodome tqdm
```

## 📁 Estrutura do Projeto

```
Five Escrow/
├── auto.py              # Script principal de automação
├── escrow.py            # Core do sistema de decriptação
├── watermark.py         # Sistema de marca d'água
├── instalador.bat       # Instalador automático
├── grant_cache.json     # Cache de chaves
├── assets/              # Pasta com recursos para decriptar
│   └── ZonaMods_baseEB_v1_Att2/
│       ├── fxmanifest.lua
│       └── stream/
└── out/                 # Pasta de saída dos arquivos decriptados
```

## 🎯 Como Usar

### 1. Preparação

1. **Coloque seus recursos protegidos** na pasta `assets/`
2. **Certifique-se de ter uma Server Key válida** da FiveM
3. **Execute o instalador** se for a primeira vez

### 2. Execução

```bash
python auto.py
```

### 3. Processo Automático

1. **Validação da Server Key**: O sistema verifica se sua chave é válida
2. **Carregamento de Chaves**: Baixa automaticamente todas as chaves necessárias
3. **Decriptação**: Processa todos os arquivos protegidos
4. **Organização**: Cria estrutura de pastas na pasta `out/`

## 🔧 Scripts Disponíveis

### `auto.py` - Script Principal
- **Função**: Automação completa do processo de decriptação
- **Recursos**: Interface visual, validação automática, processamento em lote
- **Uso**: `python auto.py`

### `escrow.py` - Core do Sistema
- **Função**: Decriptação individual de arquivos
- **Recursos**: Algoritmo ChaCha20, cache de chaves, validação JWT
- **Uso**: `python escrow.py -s -k <server_key>`

### `watermark.py` - Sistema de Marca d'Água
- **Função**: Adiciona marca d'água em todas as pastas
- **Recursos**: Processamento recursivo, personalização de conteúdo
- **Uso**: `python watermark.py -d <diretório>`

## 🔐 Algoritmo de Criptografia

O sistema utiliza o algoritmo **ChaCha20** para decriptação, implementado com a biblioteca `pycryptodome`. Este algoritmo oferece:

- **Alta Performance**: Decriptação rápida e eficiente
- **Segurança**: Algoritmo criptográfico robusto
- **Compatibilidade**: Totalmente compatível com o sistema FiveM

## 📊 Sistema de Cache

O `grant_cache.json` armazena:
- **Chaves de recursos** já processados
- **Tokens de acesso** para otimização
- **Metadados** de validação

## 🎨 Interface Visual

- **Cores**: Sistema de cores intuitivo para diferentes tipos de mensagens
- **Barras de Progresso**: Acompanhamento visual do processo
- **Banner**: Interface profissional e atrativa
- **Status em Tempo Real**: Informações sobre cada etapa do processo

## ⚠️ Limitações e Considerações

- **Server Key Válida**: É obrigatório ter uma Server Key ativa da FiveM
- **Recursos Protegidos**: Só funciona com recursos que você possui licença
- **Conexão Internet**: Requer conexão para validação de chaves
- **Permissões**: Pode requerer execução como administrador

## 🆘 Solução de Problemas

### Erro: "Python não encontrado"
- **Solução**: Instale o Python 3.7+ e adicione ao PATH

### Erro: "Dependências não encontradas"
- **Solução**: Execute `instalador.bat` como administrador

### Erro: "Server Key inválida"
- **Solução**: Verifique se sua Server Key está ativa e correta

### Erro: "Permissão negada"
- **Solução**: Execute como administrador

## 🔄 Atualizações

### v2.0 - Atualização Principal
- ✅ Interface visual completamente reformulada
- ✅ Sistema de cache otimizado
- ✅ Processamento paralelo implementado
- ✅ Validação automática de chaves
- ✅ Sistema de marca d'água integrado

## 📞 Suporte

- **Discord**: discord.gg/fivecommunity
- **Comunidade**: Five Community
- **Versão**: 2.0

## 📄 Licença

Este projeto é desenvolvido pela **Five Community** e está destinado ao uso legítimo de recursos FiveM com licenças válidas.

## 🙏 Créditos

### Desenvolvimento
- **Five Community** - Desenvolvimento principal
- **Equipe de Desenvolvedores** - Implementação e testes

### Bibliotecas Utilizadas
- **requests** - Comunicação HTTP
- **colorama** - Interface colorida
- **pycryptodome** - Criptografia
- **tqdm** - Barras de progresso

### Agradecimentos
- **FiveM Team** - Plataforma e sistema de escrow
- **Comunidade FiveM** - Feedback e suporte
- **Contribuidores** - Testes e melhorias

---

## 🚀 Começando Agora

1. **Clone ou baixe** este projeto
2. **Execute** `instalador.bat` como administrador
3. **Coloque** seus recursos na pasta `assets/`
4. **Execute** `python auto.py`
5. **Aguarde** a decriptação automática
6. **Aproveite** seus recursos decriptados!

---

**⚠️ IMPORTANTE**: Este sistema é destinado apenas para uso legítimo de recursos FiveM com licenças válidas. Respeite sempre os direitos autorais e termos de uso.

**🎯 Dica**: Para melhor performance, mantenha sua Server Key atualizada e execute o sistema em um ambiente com boa conexão à internet.
