# Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este projeto simula uma arquitetura híbrida de edge computing para agricultura remota, demonstrando:
- Coleta de dados de sensores IoT (temperatura, umidade, umidade do solo, luz)
- Processamento local em dispositivos edge
- Processamento avançado em nuvem
- Geração de alertas e recomendações em tempo real
- Monitoramento de recursos (bateria, armazenamento)

## Instalação

### Instalar dependências

```bash
pip install dataclasses-json
```

Ou usando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## Uso

### Executar simulação com duração padrão (60 segundos)

```bash
python agro_edge_simulator.py
```

### Executar com duração personalizada

```bash
# Executar por 10 minutos (600 segundos)
python agro_edge_simulator.py --duration 600

# Executar por 2 minutos (120 segundos)
python agro_edge_simulator.py --duration 120
```

### Opções de linha de comando

```bash
python agro_edge_simulator.py --help
```

Opções disponíveis:
- `--duration DURATION`: Duração da simulação em segundos (padrão: 60)
- `--sensors SENSORS`: Número de sensores a simular (padrão: 5)
- `--edge-devices EDGE_DEVICES`: Número de dispositivos edge (padrão: 2)

## Funcionalidades

### Sensores
- Temperatura (°C)
- Umidade do ar (%)
- Umidade do solo (%)
- Nível de luz (%)

### Processamento Edge
- Análise local de dados
- Detecção de necessidade de irrigação
- Alertas de temperatura e umidade
- Gerenciamento de bateria

### Processamento em Nuvem
- Predições usando ML simulado
- Geração de recomendações
- Armazenamento de dados
- Geração de relatórios

## Saída do Simulador

O simulador exibe:
- Configuração inicial
- Dados de sensores em tempo real
- Recomendações para cada sensor
- Status dos dispositivos edge
- Relatório final com estatísticas completas

## Licença

Veja o arquivo LICENSE para detalhes.
