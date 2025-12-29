"""
Exemplo de uso do EdgeNode
"""

from simulator.edge_node import EdgeNode, simulate_edge_heartbeat


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
    
    # Demonstrar simulate_edge_heartbeat
    print("\n--- Simulação de Heartbeat ---")
    node3 = EdgeNode(cpu_usage=50.0, mem_usage=30.0)
    print(f"EdgeNode 3 - CPU: {node3.cpu_usage}%, Mem: {node3.mem_usage}%")
    print(f"EdgeNode 3 - Consumo inicial: {node3.power_watts}W")
    
    simulate_edge_heartbeat(node3)
    print(f"EdgeNode 3 - Consumo após heartbeat: {node3.power_watts}W")
    
    # Simular mudança de carga
    node3.cpu_usage = 80.0
    node3.mem_usage = 60.0
    simulate_edge_heartbeat(node3)
    print(f"EdgeNode 3 - CPU: {node3.cpu_usage}%, Mem: {node3.mem_usage}%")
    print(f"EdgeNode 3 - Consumo atualizado: {node3.power_watts}W")


if __name__ == '__main__':
    main()
