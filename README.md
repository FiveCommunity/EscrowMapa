# **Escrow Map Decryptor - Modo Híbrido**

Este projeto agora funciona em **MODO HÍBRIDO** - tanto **SEM DEPENDÊNCIA** da chave CFX (usando grants locais) quanto **COM CHAVE CFX** para quebrar e obter grants adicionais!

## **✨ NOVA FUNCIONALIDADE: Modo Híbrido Local + CFX**

O sistema agora **combina o melhor dos dois mundos**:
- ✅ **Modo Local**: Usa grants do arquivo `Grants.txt` (funciona offline)
- ✅ **Modo CFX**: Conecta com servidor para obter grants adicionais
- ✅ **Modo Híbrido**: Combina ambos automaticamente

## **🚀 Como Funciona Agora:**

### **Modo Local (Padrão):**
1. **Coloque seus mapas** na pasta `./assets`
2. **Execute escaneamento automático** - usa apenas grants locais
3. **Sistema detecta e descriptografa** automaticamente

### **Modo CFX (Com Chave):**
1. **Coloque seus mapas** na pasta `./assets`
2. **Execute com chave CFX** - obtém grants do servidor
3. **Sistema quebra e descriptografa** tudo

### **Modo Híbrido (Recomendado):**
1. **Coloque seus mapas** na pasta `./assets`
2. **Execute com chave CFX** - combina local + servidor
3. **Sistema usa grants locais + obtém extras do CFX**

## **Requisitos:**
Python: 3.1x
Instale as dependências: `pip install requests colorama pycryptodome`

## **🚀 Comandos Principais:**

### **Modo Local (Sem CFX):**
```bash
# Escaneamento automático apenas com grants locais
python escrow.py --auto-scan

# Script automático local
python auto.py
```

### **Modo CFX (Com Chave):**
```bash
# Escaneamento automático com chave CFX
python escrow.py --auto-scan -k cfxk_SUA_CHAVE_AQUI

# Script automático com chave CFX
python auto.py cfxk_SUA_CHAVE_AQUI
```

### **Modo Híbrido (Recomendado):**
```bash
# Combina grants locais + CFX automaticamente
python escrow.py --auto-scan -k cfxk_SUA_CHAVE_AQUI

# Ou use o script automático
python auto.py cfxk_SUA_CHAVE_AQUI
```

### **Gerenciamento de Grants:**

#### **Adicionar um Grant:**
```bash
python escrow.py --add-grant [RESOURCE_ID] [GRANT_KEY]
```

#### **Remover um Grant:**
```bash
python escrow.py --remove-grant [RESOURCE_ID]
```

#### **Visualizar Grants Existentes:**
```bash
python escrow.py -s
```

#### **Importar Grants Locais:**
```bash
python escrow.py --import-grants
```

### **Descriptografia Manual:**

#### **Descriptografar um Diretório:**
```bash
python escrow.py -d [CAMINHO_DO_MAPA]
```

#### **Descriptografar um Arquivo:**
```bash
python escrow.py -f [CAMINHO_DO_ARQUIVO]
```

## **📁 Estrutura de Pastas:**
```
escrow-map-decryptor/
├── assets/              # Coloque seus mapas aqui
│   ├── mapa1/
│   │   └── .fxap       # Arquivo principal do mapa
│   ├── mapa2/
│   │   └── .fxap
│   └── Grants.txt      # Grants locais (JWT)
├── out/                 # Arquivos descriptografados
├── grant_cache.json     # Cache de grants (local + CFX)
└── escrow.py            # Script principal
```

## **💡 Exemplo de grant_cache.json:**
```json
{
  "12345": "abcdef1234567890abcdef1234567890abcdef12",
  "67890": "fedcba0987654321fedcba0987654321fedcba09"
}
```

## **🔄 Fluxo de Trabalho Recomendado:**

### **Opção 1: Modo Híbrido (RECOMENDADO)**
1. **Coloque mapas** na pasta `assets/`
2. **Execute com chave CFX:**
   ```bash
   python escrow.py --auto-scan -k cfxk_SUA_CHAVE_AQUI
   ```
3. **Sistema combina automaticamente:**
   - ✅ Grants locais do `Grants.txt`
   - ✅ Grants adicionais do CFX
   - ✅ Descriptografa tudo

### **Opção 2: Modo Local (Offline)**
1. **Coloque mapas** na pasta `assets/`
2. **Execute modo local:**
   ```bash
   python escrow.py --auto-scan
   ```
3. **Sistema usa apenas grants locais**

### **Opção 3: Modo CFX (Online)**
1. **Coloque mapas** na pasta `assets/`
2. **Execute modo CFX:**
   ```bash
   python escrow.py --auto-scan -k cfxk_SUA_CHAVE_AQUI
   ```
3. **Sistema obtém grants do servidor**

## **✅ Vantagens do Modo Híbrido:**
- ✅ **Sem dependência da CFX** (modo local)
- ✅ **Funciona offline** (grants locais)
- ✅ **Quebra com chave CFX** (modo servidor)
- ✅ **Combina ambos automaticamente**
- ✅ **Controle total sobre grants**
- ✅ **Mais rápido e confiável**
- ✅ **Sem limites de API** (modo local)
- ✅ **🆕 Detecção automática de recursos**
- ✅ **🆕 Escaneamento inteligente da pasta assets**
- ✅ **🆕 Modo híbrido local + CFX**

## **🔍 Como o Sistema Híbrido Funciona:**

1. **Detecta** todos os arquivos `.fxap` na pasta `assets/`
2. **Importa grants locais** do arquivo `Grants.txt`
3. **Se tiver chave CFX**, conecta com servidor para grants adicionais
4. **Combina todos os grants** (local + CFX)
5. **Verifica** se existem grants para cada recurso
6. **Descriptografa automaticamente** os recursos com grants
7. **Lista** os recursos que precisam de grants
8. **Guia** você para adicionar grants faltantes

## **🎯 Exemplos de Uso:**

### **Modo Local (Offline):**
```bash
python auto.py
```

### **Modo CFX (Online):**
```bash
python auto.py cfxk_1Gqh4rzXDTC2Q7esH4qaX_4E0TpE
```

### **Modo Híbrido (Recomendado):**
```bash
python escrow.py --auto-scan -k cfxk_1Gqh4rzXDTC2Q7esH4qaX_4E0TpE
```

## **Nota:**
- **Modo Local**: Funciona offline, usa apenas grants do `Grants.txt`
- **Modo CFX**: Funciona online, obtém grants do servidor
- **Modo Híbrido**: Combina ambos para máxima compatibilidade
- Os grants locais têm prioridade sobre os do CFX
