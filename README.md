# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador foi desenvolvido para modelar arquiteturas de edge computing em ambientes agrícolas remotos, onde o consumo de energia é um fator crítico.

## Características

### EdgeNode

Representa um nó de computação de borda (edge computing) com simulação de consumo de energia.

**Atributos:**
- `power_watts` (float): Consumo de energia em watts. Valor padrão: 12.5W
- `cpu_usage` (float): Percentual de uso de CPU (0-100). Valor padrão: 0.0
- `mem_usage` (float): Percentual de uso de memória (0-100). Valor padrão: 0.0

### simulate_edge_heartbeat()

Função que simula o heartbeat de um nó edge e atualiza o consumo de energia com base no uso de CPU e memória.

**Fórmula de cálculo:**
```
power_watts = 12.5 + (cpu_usage * 0.2) + (mem_usage * 0.1)
```

**Parâmetros:**
- `node` (EdgeNode): O nó a ter seu consumo atualizado

## Uso

```python
from simulator.edge_node import EdgeNode, simulate_edge_heartbeat

# Criar um nó com consumo padrão (12.5W)
node = EdgeNode()

# Criar um nó com consumo customizado
node = EdgeNode(power_watts=15.0)

# Criar um nó com CPU e memória em uso
node = EdgeNode(cpu_usage=50.0, mem_usage=30.0)

# Atualizar o consumo de energia baseado no uso de recursos
simulate_edge_heartbeat(node)
print(f"Consumo: {node.power_watts}W")  # 25.5W
```

## Executar Exemplo

```bash
python example.py
```

## Testes

```bash
python -m unittest discover tests
```

## Importância do Consumo de Energia

Em ambientes agrícolas remotos, a eficiência energética é fundamental devido a:
- Limitações de infraestrutura elétrica
- Dependência de energia solar/baterias
- Custos operacionais
- Sustentabilidade ambiental
