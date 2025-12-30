# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simulador completo de uma arquitetura híbrida de conectividade e edge computing projetada para **fazendas remotas** na LATAM, combinando **Starlink** como link primário, failover 4G, LoRa mesh, processamento local com inferência de borda e integração simulada do **Cambium NSE3000** (Network Service Edge) para QoS, segmentação VLAN, segurança zero-trust e backhaul seguro.

O objetivo é validar resiliência, baixa latência e ganho de produtividade (+30% simulado) em cenários "fora do mapa", onde fibra não chega.

## Características Principais

- **Integração NSE3000**: Simulação de QoS por tipo de dado, segmentação VLAN (OT/IT), políticas zero-trust e logging
- **Edge Computing**: Inferência local (ex.: análise de imagens para colheita) com cache resiliente
- **SD-WAN Híbrido**: Seleção inteligente de links (Starlink primário, 4G failover, LoRa para baixa largura)
- **Telemetria Multi-Tipo**: Suporte a temperatura, umidade, imagens, atuadores e dados críticos
- **Resiliência**: Failover automático, chaos testing e recuperação de nós edge
- **Saída Controlada**: Prints no loop principal comentados; dashboard a cada 5 ciclos + relatório final
- Rede híbrida: **Starlink** (primário) + **4G backup** + **LoRa mesh** (baixa largura)
- Edge computing com 2 nós active-active (k3s-like), heartbeat e failover de nó
- Geração de telemetria multi-tipo: temperatura, umidade, solo, imagens (visão computacional), atuadores
- Inferência local para decisões autônomas (ex.: colheita baseada em confiança de imagem)
- Testes de caos: falha de link, falha de nó, pico de tráfego
- Exportação JSON pronta para mapeamento de deploy real

## Requisitos

- Python 3.10 ou superior

## Uso

### Execução básica (duração padrão de 120 segundos)

```bash
python3 farm_simulator.py
