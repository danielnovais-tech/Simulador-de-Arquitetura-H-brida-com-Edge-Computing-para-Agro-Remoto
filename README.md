# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador foi desenvolvido para modelar arquiteturas de edge computing em ambientes agrícolas remotos, onde o consumo de energia é um fator crítico.

## Características

### EdgeNode

Representa um nó de computação de borda (edge computing) com simulação de consumo de energia.

**Atributos:**
- `power_watts` (float): Consumo de energia em watts. Valor padrão: 12.5W
- `cpu_usage` (float): Percentual de uso de CPU (0-100). Valor padrão: 0.0
- `mem_usage` (float): Percentual de uso de memória (0-100). Valor padrão: 0.0

### simulate_edge_heartbeat()

Função que simula o heartbeat de um nó edge e atualiza o consumo de energia com base no uso de CPU e memória.

**Fórmula de cálculo:**
```
power_watts = 12.5 + (cpu_usage * 0.2) + (mem_usage * 0.1)
```

**Parâmetros:**
- `node` (EdgeNode): O nó a ter seu consumo atualizado

## Uso

```python
from simulator.edge_node import EdgeNode, simulate_edge_heartbeat

# Criar um nó com consumo padrão (12.5W)
node = EdgeNode()

# Criar um nó com consumo customizado
node = EdgeNode(power_watts=15.0)

# Criar um nó com CPU e memória em uso
node = EdgeNode(cpu_usage=50.0, mem_usage=30.0)

# Atualizar o consumo de energia baseado no uso de recursos
simulate_edge_heartbeat(node)
print(f"Consumo: {node.power_watts}W")  # 25.5W
```

## Executar Exemplo

```bash
python example.py
Simula rede híbrida, edge computing resiliente e testes de validação para agricultura remota.

## Descrição

Este simulador implementa um sistema de edge computing para agricultura remota, permitindo comparar o desempenho entre processamento local (edge) e processamento na nuvem (cloud). O simulador mede o tempo de decisão para inferências locais versus envio para a nuvem.

## Características

- **Métricas de Tempo de Decisão Edge**: Mede quanto tempo leva para processar inferência local vs. enviar para nuvem
- **KPIs Automáticos**: Rastreamento de métricas de desempenho usando média móvel exponencial (EMA)
- **Simulação de Sensores**: Dados simulados de sensores agrícolas (temperatura, umidade, umidade do solo, intensidade de luz)
- **Comparação Edge vs Cloud**: Análise de desempenho entre processamento local e remoto
- **Latência de Rede Simulada**: Simula atrasos de rede realistas para comunicação com a nuvem

## Instalação

```bash
# Clone o repositório
git clone https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto.git

# Entre no diretório
cd Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto

# Instale dependências (apenas Python 3.7+ necessário)
pip install -r requirements.txt
```

## Uso

### Execução Rápida

```bash
python3 demo.py
```

### Uso Programático

```python
from edge_simulator import EdgeComputingSimulator

# Cria o simulador
simulator = EdgeComputingSimulator()

# Processa inferência no edge
result = simulator.process_edge_inference()
print(f"Tempo de inferência edge: {result['inference_time_ms']:.1f} ms")

# Processa inferência na nuvem
result = simulator.process_cloud_inference()
print(f"Tempo total cloud: {result['total_time_ms']:.1f} ms")

# Visualiza KPIs
simulator.print_kpis()
```

## Exemplo de Saída

```
[Edge] Inferência local concluída em 14.7 ms
[Cloud] Inferência na nuvem concluída em 284.9 ms (latência rede: ~260.3 ms)

KPIs do Simulador de Edge Computing
Total de inferências: 6
Tempo médio Edge: 4.42 ms
Tempo médio Cloud: 118.23 ms
Aceleração Edge vs Cloud: 26.72x mais rápido
```

## Métricas de Tempo de Decisão

O método `process_edge_inference` implementa a medição de tempo conforme especificado:

```python
def process_edge_inference(self):
    start = time.time()
    # ... processamento atual ...
    inference_time = (time.time() - start) * 1000  # ms
    print(f"[Edge] Inferência local concluída em {inference_time:.1f} ms")
    self.kpis.setdefault('avg_inference_time', 0)
    self.kpis['avg_inference_time'] = (
        self.kpis.get('avg_inference_time', 0) * 0.9 + inference_time * 0.1
    )
```

## Testes

```bash
python -m unittest discover tests
```

## Importância do Consumo de Energia

Em ambientes agrícolas remotos, a eficiência energética é fundamental devido a:
- Limitações de infraestrutura elétrica
- Dependência de energia solar/baterias
- Custos operacionais
- Sustentabilidade ambiental
Execute os testes unitários:

```bash
python3 test_edge_simulator.py
```

## Estrutura do Projeto

```
.
├── edge_simulator.py       # Módulo principal do simulador
├── demo.py                 # Demonstração de uso
├── test_edge_simulator.py  # Testes unitários
├── requirements.txt        # Dependências
└── README.md              # Esta documentação
```

## Licença

Veja o arquivo [LICENSE](LICENSE) para detalhes.
## 📋 Descrição

Este simulador foi desenvolvido para validar arquiteturas híbridas de edge computing aplicadas ao setor agrícola remoto. Ele simula:

- **Conectividade Híbrida**: Links Starlink, 4G/LTE e LoRa com failover automático (SD-WAN)
- **Edge Computing Resiliente**: Nós K3s em configuração active-active com heartbeat
- **Telemetria IoT**: Sensores de temperatura, umidade, solo, câmeras e atuadores
- **Inferência Local**: Processamento de visão computacional para colheita autônoma
- **Segurança**: Simulação NSE3000 com VLANs, IPsec e zero trust
- **Testes de Caos**: Validação de resiliência com falhas controladas

## 🚀 Uso

### Executar Simulação Principal

```bash
python3 simulador_agro_edge.py
```

A simulação executa por 2 minutos (120 segundos) e gera:
- Dashboard de status em tempo real
- Testes de caos periódicos
- Relatório final com KPIs
- Arquivo de configuração `agro_edge_deploy.json`

### Componentes Simulados

#### 1. Links de Rede
- **Starlink-001**: Primário, 45ms latência, 150 Mbps
- **4G-Rural-01**: Backup, 85ms latência, 30 Mbps
- **LoRa-Mesh-01**: Local, 120ms latência, 0.05 Mbps

#### 2. Nós Edge
- **edge-01** e **edge-02**: K3s + MQTT em active-active
- Monitoramento de CPU, memória e heartbeat

#### 3. Sensores/Atuadores
- Temperatura, umidade, solo, câmeras, colheitadeiras
- Hash SHA-256 para integridade dos dados

## 📊 KPIs Monitorados

- **Disponibilidade**: Meta >99.5%
- **Latência Média**: Meta <50ms
- **Failovers**: Contagem de recuperações automáticas
- **Mensagens**: Entregues vs. perdidas
- **Ganho de Produtividade**: Meta +30%

## 🧪 Testes de Caos

O simulador executa testes controlados de:
- **link_failure**: Falha do link primário
- **node_failure**: Falha de nó edge
- **traffic_spike**: Pico de tráfego (50 mensagens)

Cada teste mede o tempo de recuperação (SLA: <5s).

## 🔧 Requisitos

- Python 3.7+
- Bibliotecas padrão (sem dependências externas)

## 📦 Saída

O simulador gera `agro_edge_deploy.json` com:
- Configuração completa da arquitetura
- Status dos componentes
- KPIs finais
- Configuração NSE3000 (VLANs, túneis IPsec)

## 🎯 Próximos Passos Recomendados

1. Validar NSE3000 com vendor (L3 switch, firewall, gateway)
2. Inventário completo de sensores/atuadores
3. Piloto em 1 fazenda com 2 nós edge
4. Testes de caos em ambiente controlado
5. Medição contínua de KPIs (+30% produtividade)

## 📄 Licença

Ver arquivo LICENSE
# Hybrid Edge Computing Architecture for Remote Agriculture / Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

**Complete resilient architecture simulation with network failover, edge orchestration, telemetry, chaos testing, and observability**  
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![CI](https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto/actions/workflows/ci.yml/badge.svg)](https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto/actions/workflows/ci.yml)

This simulator models a hybrid connectivity and edge computing architecture designed for **remote farms** in LATAM, combining **Starlink** as primary link, 4G failover, LoRa mesh, local processing with edge inference, and simulated integration of **Cambium NSE3000** (Network Service Edge) for QoS, VLAN segmentation, zero-trust security, and secure backhaul.  

The goal is to validate resilience, low latency, and productivity gains (+30% simulated) in "off-the-map" scenarios where fiber isn't available. (Nota: Esta documentação está principalmente em inglês para acessibilidade global; seções chave em português disponíveis sob solicitação.)

## 🎯 Key Performance Indicators (KPIs)
This system validates and achieves the following KPIs:
- ✅ **>99.5% Availability** - High availability through network resilience
- ✅ **<5s Failover Time** - Rapid network failover between Starlink/4G/LoRa
- ✅ **<50ms Latency** - Low latency communication for real-time control
- ✅ **+30% Productivity Gain** - Autonomous harvest optimization

## 🏗️ Architecture Overview

┌─────────────────────────────────────────────────────────────────┐
│ Remote Agriculture Site                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐             │
│ │ Starlink     │ │ 4G           │ │ LoRa         │             │
│ │ (Primary)    │ │ (Secondary)  │ │ (Fallback)   │             │
│ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘             │
│        └────────────┬─────────────────┬─────┘                   │
│                     │                                           │
│             Network Resilience Manager                          │
│             (Auto-failover <5s)                                 │
│                     │                                           │
│        ┌────────────┴────────────┐                              │
│        │                         │                              │
│ ┌────▼─────┐ ┌─────▼────┐ ┌─────▼────┐                         │
│ │ K3s      │ │ MQTT     │ │ NSE3000  │                         │
│ │ Edge     │◄──────────►│ Telemetry│ │ (QoS/Security)          │
│ │ Cluster  │ │ Broker   │ └──────────┘                         │
│ └────┬─────┘ └─────┬────┘                                       │
│      │             │                                            │
│ ┌────▼─────────────────────────▼────┐                           │
│ │ IoT Sensors & Actuators          │                           │
│ │ (Soil, Climate, Crop Monitoring) │                           │
│ └───────────────────────────────────┘                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Security Layer (Zero-Trust)                                     │
│ NSE3000 Policies | Authentication | Encryption                  │
├─────────────────────────────────────────────────────────────────┤
│ Observability (Prometheus + Grafana)                            │
│ Metrics | Logging | Alerting | Dashboards                       │
└─────────────────────────────────────────────────────────────────┘


## 🚀 Features
### 1. **Network Resilience Layer**
- **Multi-network Failover**: Automatic switching between Starlink, 4G, and LoRa
- **Health Monitoring**: Continuous health checks on all network interfaces
- **Sub-5s Failover**: Meets strict failover time requirements
- **Latency Optimization**: Maintains <50ms latency for critical operations
- **SD-WAN Híbrido**: Seleção inteligente de links (Starlink primário, 4G failover, LoRa para baixa largura)

### 2. **Edge Computing with K3s**
- **Lightweight Kubernetes**: K3s cluster orchestration optimized for edge
- **Workload Management**: Automatic workload distribution across edge nodes
- **Resource Optimization**: Efficient CPU, memory, and storage allocation
- **High Availability**: Node failure recovery and workload rescheduling
- **Integração NSE3000**: Simulação de QoS por tipo de dado, segmentação VLAN (OT/IT), políticas zero-trust e logging

### 3. **MQTT Telemetry System**
- **Real-time Data Collection**: Agriculture sensor data (soil, climate, crops)
- **Message Buffering**: Resilient to network interruptions
- **Data Validation**: Quality checks on sensor readings
- **Scalable Architecture**: Handles thousands of sensors
- **Telemetria Multi-Tipo**: Suporte a temperatura, umidade, imagens, atuadores e dados críticos

### 4. **Chaos Engineering**
- **Network Failure Simulation**: Test failover mechanisms
- **Node Failure Tests**: Validate cluster resilience
- **Latency Injection**: Performance under degraded conditions
- **Partition Testing**: Split-brain scenario validation
- **Resource Exhaustion**: Stress testing
- **Testes de Caos**: Falha de link, falha de nó, pico de tráfego

### 5. **Observability & Monitoring**
- **Prometheus Metrics**: Real-time KPI tracking
- **Grafana Dashboards**: Visual monitoring and alerting
- **Audit Logging**: Complete system activity logs
- **Health Checks**: Component status monitoring

### 6. **Security (NSE3000 & Zero-Trust)**
- **Zero-Trust Architecture**: Never trust, always verify
- **Role-Based Access Control**: Granular permissions
- **Session Management**: Secure authentication
- **Certificate Management**: TLS/SSL encryption
- **Audit Trail**: Complete security event logging

### 7. **Agriculture Data & Validation**
- **Realistic Sensor Data**: Simulated agriculture sensor readings
- **Crop Growth Modeling**: Multi-stage crop development
- **Autonomous Harvest Decisions**: AI-driven harvest optimization
- **Productivity Metrics**: Real productivity gain calculations
- **Inferência Local**: Análise de imagens para colheita com cache resiliente

## 📦 Installation
### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto.git
cd Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto
# Install dependencies
pip install -r requirements.txt
# Or install in development mode
pip install -e .
```

## 🧪 Testing
This project includes a comprehensive test suite with >80% code coverage to ensure code quality and prevent regressions.

### Running Tests Locally

Run all tests with verbose output:
```bash
pytest tests/ -v
```

Run tests for the main simulator:
```bash
pytest tests/test_agro_edge.py -v
```

### Code Coverage

Check code coverage:
```bash
pytest tests/ --cov=agro_edge_simulator --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov/` directory. Open `htmlcov/index.html` in your browser to view detailed coverage information.

View coverage in terminal:
```bash
pytest tests/ --cov=agro_edge_simulator --cov-report=term-missing
```

### CI/CD Pipeline

The project uses GitHub Actions for continuous integration:
- **Triggers**: Automatic on push to `main` branch and pull requests
- **Python versions tested**: 3.9, 3.10, 3.11
- **Test requirements**: All tests must pass before merge
- **Coverage target**: >80% code coverage

Check the CI status badge at the top of this README or visit the [Actions tab](https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto/actions) to see test results.
