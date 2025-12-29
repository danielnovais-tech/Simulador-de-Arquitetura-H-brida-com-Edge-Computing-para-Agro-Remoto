# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador foi desenvolvido para modelar arquiteturas de edge computing em ambientes agrícolas remotos, onde o consumo de energia é um fator crítico.

## Características

### EdgeNode

Representa um nó de computação de borda (edge computing) com simulação de consumo de energia.

**Atributos:**
- `power_watts` (float): Consumo de energia em watts. Valor padrão: 12.5W

## Uso

```python
from simulator.edge_node import EdgeNode

# Criar um nó com consumo padrão (12.5W)
node = EdgeNode()

# Criar um nó com consumo customizado
node = EdgeNode(power_watts=15.0)
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
