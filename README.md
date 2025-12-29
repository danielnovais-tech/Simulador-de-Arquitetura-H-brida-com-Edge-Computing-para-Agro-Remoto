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
