# Simulador-de-Arquitetura-Híbrida-com-Edge-Computing-para-Agro-Remoto
Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador implementa uma arquitetura híbrida com edge computing para monitoramento remoto de fazendas. O sistema simula:

- Leitura de sensores agrícolas (temperatura, umidade, luminosidade, pH do solo)
- Processamento de dados em nós edge
- Envio de dados processados para a nuvem
- Detecção de alertas baseada em condições dos sensores

## Requisitos

- Python 3.6 ou superior

## Uso

### Execução básica (duração padrão de 120 segundos)

```bash
python3 farm_simulator.py
```

### Execução com duração personalizada

Para executar a simulação por 10 minutos (600 segundos):

```bash
python3 farm_simulator.py --duration 600
```

Para executar a simulação por 1 minuto (60 segundos):

```bash
python3 farm_simulator.py --duration 60
```

### Ajuda

Para ver todas as opções disponíveis:

```bash
python3 farm_simulator.py --help
```

## Parâmetros

- `--duration`: Duração da simulação em segundos (padrão: 120)

## Exemplo de Saída

```
=== Iniciando Simulação de Fazenda Inteligente ===
Duração: 120 segundos (2.0 minutos)
Sensores: temperatura, umidade, luminosidade, pH_solo
Nós Edge: edge_node_1, edge_node_2, edge_node_3
Conectividade Cloud: Sim
==================================================

[0.0s] Iteração 1
  Dados: Temp=25.3°C, Umidade=65.2%, Luz=78.5%, pH=6.8
  Processado em: edge_node_2
  Cloud: ✓ Enviado
...
```
