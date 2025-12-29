# Simulador-de-Arquitetura-Híbrida-com-Edge-Computing-para-Agro-Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador demonstra uma arquitetura híbrida para agricultura remota, combinando:
- **Edge Computing**: Processamento local em nós distribuídos
- **Cloud Computing**: Análise agregada e armazenamento centralizado
- **Resiliência**: Capacidade de recuperação de falhas
- **Sensores IoT**: Monitoramento de múltiplos parâmetros agrícolas

## Características

- ✅ Simulação de sensores agrícolas (temperatura, umidade do solo, pH, etc.)
- ✅ Processamento distribuído em nós Edge
- ✅ Sincronização com servidor Cloud
- ✅ Detecção de alertas em tempo real
- ✅ Teste de resiliência com falhas e recuperação automática
- ✅ Analytics agregado na nuvem

## Como Executar

```bash
python3 agro_edge_simulator.py
```

## Requisitos

- Python 3.6 ou superior
- Bibliotecas padrão do Python (sem dependências externas)

## Arquitetura

O simulador implementa uma arquitetura de três camadas:

1. **Camada de Sensores**: 15 sensores distribuídos coletando dados
2. **Camada Edge**: 3 nós de processamento local com buffer e detecção de alertas
3. **Camada Cloud**: Servidor centralizado para analytics avançado

## Tipos de Sensores Simulados

- Temperatura
- Umidade do Solo
- Umidade do Ar
- Luminosidade
- pH do Solo
- Precipitação
