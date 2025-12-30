# Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto
Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador demonstra uma arquitetura híbrida de edge computing para agricultura remota, incluindo:
- Nós de edge computing distribuídos em diferentes localizações de fazendas
- Sensores IoT para monitoramento (temperatura, umidade, umidade do solo)
- Servidor cloud para processamento centralizado
- Rede híbrida com processamento distribuído e resiliente

## Uso

### Execução básica (duração padrão = 300 segundos ≈ 5 minutos)

```bash
python agro_edge_simulator.py
```

### Execução com duração personalizada

```bash
python agro_edge_simulator.py --duration 60  # 60 segundos
```

### Execução com configuração personalizada

```bash
# Simular com 5 nós edge, 4 sensores por nó, 30% de dados ao cloud
python agro_edge_simulator.py --num-edges 5 --sensors-per-edge 4 --cloud-forward-ratio 0.3
```

### Opções disponíveis

```bash
python agro_edge_simulator.py --help
```

**Parâmetros:**
- `--duration SEGUNDOS`: Duração da simulação (padrão: 300s, máx: 86400s)
- `--num-edges N`: Número de nós edge (padrão: 3)
- `--sensors-per-edge N`: Sensores IoT por nó edge (padrão: 3)
- `--cloud-forward-ratio X`: Fração de dados enviados ao cloud, 0-1 (padrão: 0.2)
- `--log-level LEVEL`: Nível de log: DEBUG, INFO, WARNING, ERROR (padrão: WARNING)

## Componentes da Simulação

- **Nós Edge**: Processam dados localmente em diferentes fazendas (configurável)
- **Sensores IoT**: Coletam dados de temperatura, umidade e umidade do solo (configurável)
- **Servidor Cloud**: Recebe dados críticos para processamento centralizado
- **Arquitetura Híbrida**: Distribuição configurável entre processamento edge e cloud

## Características

### Mapeamento Geográfico
Os sensores são automaticamente mapeados aos edge nodes baseado em proximidade geográfica, simulando uma implantação realista.

### Tamanhos de Dados Realistas
Diferentes tipos de sensores geram payloads de tamanhos diferentes:
- **Temperatura**: 80-180 bytes (dados simples)
- **Umidade**: 120-220 bytes (metadados adicionais)
- **Umidade do Solo**: 180-320 bytes (múltiplos parâmetros)

### Simulação de Recursos
CPU e memória dos edge nodes variam dinamicamente baseado na carga de trabalho, com padrões realistas de uso.

## Saída

O simulador fornece:
- Status em tempo real a cada 30 segundos
- Métricas de CPU e memória dos nós edge
- Estatísticas de dados processados
- Eficiência do edge computing
- Resumo final completo

## Testes

Execute os testes unitários com:

```bash
python -m unittest discover tests
```

Ou com verbosidade:

```bash
python -m unittest discover tests -v
```

## Exemplos de Uso

### Simulação pequena (teste rápido)
```bash
python agro_edge_simulator.py --duration 30 --num-edges 2 --sensors-per-edge 2
```

### Simulação média (padrão)
```bash
python agro_edge_simulator.py
```

### Simulação grande (múltiplas fazendas)
```bash
python agro_edge_simulator.py --duration 600 --num-edges 10 --sensors-per-edge 5 --cloud-forward-ratio 0.15
```

### Modo debug com logs detalhados
```bash
python agro_edge_simulator.py --duration 60 --log-level DEBUG
```

## Limitações

- Assume rede ideal sem simulação de latência ou falhas de rede
- Não simula perda de pacotes ou problemas de conectividade
- Edge nodes não falham durante a simulação (sempre ativos)
- Dados dos sensores são gerados aleatoriamente dentro de faixas realistas

## Estendendo o Simulador

### Adicionando Novos Tipos de Sensores

1. No método `generate_reading()` da classe `IoTSensor`, adicione uma nova condição:
```python
elif self.sensor_type == 'novo_sensor':
    value = random.uniform(min_value, max_value)
```

2. No método `_estimate_data_size()` da classe `AgroEdgeSimulator`, adicione:
```python
elif sensor_type == 'novo_sensor':
    return random.randint(min_bytes, max_bytes)
```

### Implementando Falhas de Nós

Para simular resiliência, você pode adicionar falhas aleatórias aos edge nodes modificando o método `simulate_cycle()`:

```python
# Exemplo: 1% de chance de falha por ciclo
if random.random() < 0.01:
    edge_node.active = False
```
