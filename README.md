# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simulador completo de uma arquitetura híbrida de conectividade e edge computing projetada para **fazendas remotas** na LATAM, combinando **Starlink** como link primário, failover 4G, LoRa mesh, processamento local com inferência de borda e integração simulada do **Cambium NSE3000** (Network Service Edge) para QoS, segmentação VLAN, segurança zero-trust e backhaul seguro.

O objetivo é validar resiliência, baixa latência e ganho de produtividade (+30% simulado) em cenários "fora do mapa", onde fibra não chega.

## Características Principais

- Rede híbrida: **Starlink** (primário) + **4G backup** + **LoRa mesh** (baixa largura)
- SD-WAN simulado com failover automático e recuperação
- Edge computing com 2 nós active-active (k3s-like), heartbeat e failover de nó
- Geração de telemetria multi-tipo: temperatura, umidade, solo, imagens (visão computacional), atuadores
- Inferência local para decisões autônomas (ex.: colheita baseada em confiança de imagem)
- Integração NSE3000 (Cambium): QoS por tipo de dado, VLAN OT/IT, túneis IPsec, políticas zero-trust
- Testes de caos: falha de link, falha de nó, pico de tráfego
- Dashboard a cada 5 ciclos + relatório final com KPIs
- Exportação JSON pronta para mapeamento de deploy real

## Arquitetura Simulada

```
[ Sensores IoT no campo ]
         ↓ (telemetria)
   [ Nós Edge k3s-like ] ← heartbeat + failover
    ↑ QoS + VLAN + Zero-Trust ← NSE3000 Simulator
         ↓ (SD-WAN)
[ Starlink (primário) ] ─┬─ [ 4G Backup ]
                         └─ [ LoRa Mesh ]
         ↓ (backhaul seguro)
    [ Cloud Agro (IPsec) ]
```

## Como Executar

### Requisitos
- Python 3.10 ou superior
- Sem dependências externas (usa apenas biblioteca padrão)

### Execução básica (2 minutos de simulação)
```bash
python3 agro_edge_simulator.py
```

### Execução com duração personalizada
Edite a linha no `main()`:
```python
farm_simulator.run_simulation(duration=600)  # 10 minutos
```

Adicione suporte a argumentos (recomendado):
```python
# No topo do arquivo, após os imports
import argparse

# Dentro de main():
parser = argparse.ArgumentParser(description="Simulador Agro Edge Híbrido")
parser.add_argument('--duration', type=int, default=300, help='Duração em segundos')
args = parser.parse_args()

farm_simulator.run_simulation(duration=args.duration)
```

Então execute:
```bash
python3 agro_edge_simulator.py --duration 600
```

## Dicas para rodar e observar melhor

A saída é verbosa → rode em um terminal grande ou redirecione para arquivo se quiser analisar depois:

```bash
python agro_edge_simulator.py > simulacao_$(date +%Y%m%d_%H%M).log
```

Isso cria arquivos de log com timestamp (ex.: `simulacao_20231229_1630.log`) para análise pós-execução.

## Saída Esperada

- Configuração inicial do NSE3000 (VLANs, IPsec, zero-trust)
- Ciclos com prints de eventos (failover, inferência, caos)
- Dashboard a cada 5 ciclos mostrando:
  - Status de links e política SD-WAN
  - Saúde dos nós edge (CPU, memória, k3s/MQTT)
  - KPIs: disponibilidade, latência média, failovers, mensagens, produtividade
- Relatório final + avaliação de metas (SLA ≥99.5%, latência ≤50 ms, produtividade ≥30%)
- Arquivo `agro_edge_deploy.json` gerado com toda a configuração

### Métricas e Metas

| Métrica | Meta | Resultado Típico |
|---------|------|------------------|
| Disponibilidade | ≥99.5% | 99.5–100% |
| Latência média | ≤50 ms | ~50–70 ms |
| Ganho de produtividade | ≥30% | +30–35% |
| Tempo de recuperação | <5 segundos | 1–4 s (caos) |
| Mensagens perdidas | <1% | ~0.5–1% |

## Próximos Passos Recomendados

1. Validar comportamento com NSE3000 real (cnMaestro API + cnMatrix/cnPilot)
2. Mapear para hardware edge: Raspberry Pi 5 / NVIDIA Jetson + k3s + Mosquitto MQTT
3. Adicionar exportação Prometheus/Grafana para visualização real-time
4. Piloto em campo: 1 pivô central ou talhão com 10–20 sensores
5. Evoluir inferência: YOLOv8n/TensorRT para detecção de pragas/colheita

## Licença

MIT License – veja o arquivo LICENSE

---

Inspirado em conversas sobre integração Starlink + Cambium NSE3000 para conectividade crítica em áreas remotas (LATAM, agro, mineração, offshore).

**Vamos decolar essa arquitetura para o campo! 🚀**