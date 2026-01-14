# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação para agricultura remota.

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
