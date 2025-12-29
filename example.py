"""
Exemplo de uso do EdgeNode
"""

from simulator.edge_node import EdgeNode


def main():
    # Criar um EdgeNode com valor padrão de consumo de energia
    node1 = EdgeNode()
    print(f"EdgeNode 1 - Consumo de energia: {node1.power_watts}W")
    
    # Criar um EdgeNode com consumo de energia customizado
    node2 = EdgeNode(power_watts=15.0)
    print(f"EdgeNode 2 - Consumo de energia: {node2.power_watts}W")
    
    # Exemplo: calcular consumo total de uma rede com múltiplos nós
    nodes = [EdgeNode() for _ in range(5)]
    total_power = sum(node.power_watts for node in nodes)
    print(f"\nRede com {len(nodes)} nós - Consumo total: {total_power}W")


if __name__ == '__main__':
    main()
