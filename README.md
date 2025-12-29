# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação com integração NSE3000 (Fortinet FortiGate) para QoS e segurança.

## Características

- **Integração NSE3000**: QoS e políticas de segurança aplicadas ao processamento de telemetria
- **Edge Computing**: Processamento de inferência na borda com análise de dados de sensores agrícolas
- **SD-WAN**: Seleção inteligente de links baseada em tipo de dado e criticidade
- **Telemetria Multi-Tipo**: Suporte para temperatura, imagens, atuadores e dados genéricos

## Arquitetura

### NSE3000 Integration
O NSE3000 (Fortinet FortiGate) está integrado ao fluxo principal de processamento:
- Aplicação de políticas QoS por tipo de dado
- Priorização via VLANs (ot_network para dados OT/agrícolas)
- Estatísticas de políticas aplicadas

### Priorização de Dados
- **Alta prioridade**: temperature, actuator (dados críticos em tempo real)
- **Média prioridade**: image (visão computacional tolerante a delay)
- **Baixa prioridade**: outros dados (humidity, etc.)

### SD-WAN
- **4G**: Dados críticos (temperatura, atuadores)
- **Satellite**: Imagens (maior banda, tolerante a latência)

## Como Usar

```bash
python3 simulator.py
```

## Saída Esperada

O simulador demonstra:
1. Configuração inicial do NSE3000
2. Processamento de diferentes tipos de telemetria
3. Aplicação de políticas QoS integradas
4. Seleção de links SD-WAN
5. Estatísticas finais de operação

## Exemplo de Integração NSE3000

```python
def apply_nse3000_policies(self, telemetry: TelemetryData):
    """Simula aplicação de QoS e segurança NSE3000 por tipo de dado"""
    if telemetry.data_type in ["temperature", "actuator"]:
        priority = "high"
    elif telemetry.data_type == "image":
        priority = "medium"
    else:
        priority = "low"
    
    print(f"[NSE3000-QoS] Aplicando prioridade '{priority}' para {telemetry.sensor_id} "
          f"({telemetry.data_type}) via VLAN ot_network")
```

## Componentes

- **TelemetryData**: Modelo de dados de telemetria
- **NSE3000**: Simulador Fortinet FortiGate para QoS/segurança
- **EdgeComputing**: Processamento de inferência com integração NSE3000
- **SDWANManager**: Gerenciador de links SD-WAN

## Licença

Ver arquivo LICENSE
