"""
Demonstração do Simulador de Edge Computing para Agro Remoto

Este script demonstra o uso do simulador, comparando tempos de 
processamento entre edge e cloud.
"""

from edge_simulator import EdgeComputingSimulator


def main():
    """Executa demonstração do simulador."""
    print("Simulador de Arquitetura Híbrida com Edge Computing")
    print("Para Agricultura Remota")
    print("\n" + "="*60 + "\n")
    
    # Cria instância do simulador
    simulator = EdgeComputingSimulator()
    
    # Executa várias inferências no edge
    print("Executando inferências no EDGE (local)...\n")
    for i in range(5):
        result = simulator.process_edge_inference()
        print(f"  Resultado {i+1}: {result['result']}\n")
    
    # Executa várias inferências na nuvem para comparação
    print("\nExecutando inferências na NUVEM...\n")
    for i in range(5):
        result = simulator.process_cloud_inference()
        print(f"  Resultado {i+1}: {result['result']}\n")
    
    # Exibe KPIs finais
    simulator.print_kpis()
    
    # Demonstra comparação direta
    print("\nComparação Direta - Mesmo dado processado em ambos locais:")
    print("-" * 60)
    
    # Gera dados de teste
    test_data = simulator._simulate_sensor_data()
    print(f"\nDados do sensor: {test_data}\n")
    
    # Processa no edge
    edge_result = simulator.process_edge_inference(test_data)
    
    # Processa na nuvem
    cloud_result = simulator.process_cloud_inference(test_data)
    
    # Compara tempos
    print(f"\nTempo Edge: {edge_result['inference_time_ms']:.1f} ms")
    print(f"Tempo Cloud: {cloud_result['total_time_ms']:.1f} ms")
    speedup = cloud_result['total_time_ms'] / edge_result['inference_time_ms']
    print(f"Edge foi {speedup:.1f}x mais rápido!\n")
    
    # KPIs finais
    simulator.print_kpis()


if __name__ == "__main__":
    main()
