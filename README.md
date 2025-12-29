# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simulador de rede híbrida que combina edge computing e cloud computing para cenários de agricultura remota, com foco em resiliência, baixa latência e eficiência no processamento de dados de sensores agrícolas.

## 📋 Descrição

Este projeto implementa um simulador completo de arquitetura híbrida que demonstra:

- **Edge Computing Resiliente**: Processamento local de dados críticos com baixa latência
- **Arquitetura Híbrida**: Combinação inteligente de processamento edge, gateway e cloud
- **Rede Híbrida**: Topologia que simula sensores IoT, nós edge, gateways e infraestrutura cloud
- **Testes de Validação**: Conjunto de testes automatizados para verificar funcionalidade e resiliência
- **Métricas e Monitoramento**: Coleta de latência, throughput e taxa de sucesso

## 🚀 Como Executar

### Pré-requisitos

- Python 3.7 ou superior
- Nenhuma dependência externa necessária (usa apenas bibliotecas padrão do Python)

### Execução Básica

1. **Clone o repositório** (se ainda não fez):
```bash
git clone https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto.git
cd Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto
```

2. **Execute o simulador**:
```bash
python3 agro_edge_simulator.py
```

### Execução com Permissões

Se necessário, torne o arquivo executável:
```bash
chmod +x agro_edge_simulator.py
./agro_edge_simulator.py
```

## ⚙️ Configuração

O simulador pode ser configurado editando o dicionário `custom_config` na função `main()`:

```python
custom_config = {
    'num_sensors': 10,              # Número de sensores IoT
    'num_edge_nodes': 3,            # Número de nós edge
    'num_cloud_nodes': 1,           # Número de nós cloud
    'num_gateway_nodes': 2,         # Número de gateways
    'edge_capacity': 100,           # Capacidade de processamento edge
    'cloud_capacity': 1000,         # Capacidade de processamento cloud
    'gateway_capacity': 50,         # Capacidade de processamento gateway
    'simulation_duration': 30,      # Duração da simulação (segundos)
    'data_generation_rate': 2.0     # Dados gerados por segundo
}
```

## 📊 Saída da Simulação

O simulador gera:

1. **Console Output**: Progresso em tempo real e relatórios detalhados
2. **Arquivo JSON**: `simulation_results.json` com métricas completas

### Exemplo de Saída

```
╔══════════════════════════════════════════════════════════════╗
║  SIMULADOR DE ARQUITETURA HÍBRIDA COM EDGE COMPUTING        ║
║  PARA AGRICULTURA REMOTA                                     ║
╚══════════════════════════════════════════════════════════════╝

Inicializando rede híbrida...
Rede inicializada com 10 sensores, 3 edge nodes, 2 gateways, e 1 cloud nodes

Executando simulação por 30 segundos...
...
RELATÓRIO DA SIMULAÇÃO
Taxa de sucesso: 98.50%
Latência média: 25.34ms

TESTES DE VALIDAÇÃO
✅ Teste 1: Existem nós ativos na rede
✅ Teste 2: Dados foram processados com sucesso
✅ Teste 3: Edge nodes processaram dados localmente
✅ Teste 4: Sistema demonstrou resiliência
✅ Teste 5: Latência dentro de limites aceitáveis

🎉 Todos os testes de validação passaram!
```

## 🏗️ Arquitetura do Sistema

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Sensores   │────▶│  Edge Nodes │────▶│  Gateways   │────▶┌──────────┐
│   (IoT)     │     │  (Processo  │     │  (Agregação)│     │  Cloud   │
│             │     │   Local)    │     │             │     │          │
└─────────────┘     └─────────────┘     └─────────────┘     └──────────┘
                           ▲                                        │
                           │          Failover / Backup             │
                           └────────────────────────────────────────┘
```

### Componentes

- **Sensores**: Geram dados agrícolas (umidade do solo, temperatura, pH, detecção de pragas)
- **Edge Nodes**: Processam dados críticos localmente com baixa latência
- **Gateways**: Agregam dados e fazem roteamento inteligente
- **Cloud**: Processamento em lote e armazenamento de longo prazo

### Estratégias de Roteamento

1. **Dados Críticos** → Edge (latência ~5-15ms)
2. **Dados Médios** → Gateway (latência ~15-30ms)
3. **Dados Baixa Prioridade** → Cloud (latência ~50-100ms)

## 🔬 Testes de Validação

O simulador inclui 5 testes automatizados:

1. ✅ Verificação de nós ativos
2. ✅ Processamento de dados
3. ✅ Funcionamento do edge computing
4. ✅ Resiliência do sistema
5. ✅ Latência aceitável

## 📈 Métricas Coletadas

- Taxa de sucesso de processamento
- Latência média por tipo de nó
- Throughput (dados processados por segundo)
- Distribuição de carga entre edge/gateway/cloud
- Taxa de recuperação de falhas

## 🛠️ Desenvolvimento

### Estrutura do Código

- `SensorData`: Classe de dados para informações de sensores
- `Node`: Representa nós da rede (sensor, edge, gateway, cloud)
- `EdgeComputingSimulator`: Classe principal do simulador
- Enums: `NodeType`, `DataPriority`

### Extensões Possíveis

- Adicionar mais tipos de sensores
- Implementar algoritmos de machine learning no edge
- Adicionar visualização gráfica em tempo real
- Integrar com sensores IoT reais
- Implementar protocolos de rede específicos (MQTT, CoAP)

## 📄 Licença

Este projeto está licenciado sob a licença especificada no arquivo LICENSE.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📞 Contato

Para questões ou sugestões, abra uma issue no repositório.
