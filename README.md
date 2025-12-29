# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação com integração NSE3000 (Cambium Network Service Edge) para QoS, segurança e SD-WAN.

## Características Principais
- **Integração NSE3000**: Simulação de QoS por tipo de dado, segmentação VLAN (OT/IT), políticas zero-trust e logging
- **Edge Computing**: Inferência local (ex.: análise de imagens para colheita) com cache resiliente
- **SD-WAN Híbrido**: Seleção inteligente de links (Starlink primário, 4G failover, LoRa para baixa largura)
- **Telemetria Multi-Tipo**: Suporte a temperatura, umidade, imagens, atuadores e dados críticos
- **Resiliência**: Failover automático, chaos testing e recuperação de nós edge
- **Saída Controlada**: Prints no loop principal comentados; dashboard a cada 5 ciclos + relatório final

## Arquitetura
- **NSE3000 (simulado)**: Aplicação dinâmica de prioridade:
  - Alta: temperatura, atuadores (dados SCADA-like)
  - Média: imagens (visão computacional)
  - Baixa: umidade, logs genéricos
- **SD-WAN**: Starlink para banda larga (imagens), 4G para baixa latência (alertas críticos)

## Como Usar
### Requisitos
- Python 3.10–3.12
- Sem dependências externas

### Execução
```bash
python3 simulador.py
