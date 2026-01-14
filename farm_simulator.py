#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Hybrid Architecture Simulator with Edge Computing for Remote Agriculture
"""

import argparse
import time
import random
from datetime import datetime


class FarmSimulator:
    """Simulates a hybrid edge computing architecture for remote agriculture monitoring"""
    
    # Alert thresholds
    TEMP_HIGH_THRESHOLD = 30  # Celsius
    HUMIDITY_LOW_THRESHOLD = 50  # Percentage
    
    # Simulation parameters
    ITERATION_INTERVAL = 2  # seconds between iterations
    
    def __init__(self):
        self.sensors = ["temperatura", "umidade", "luminosidade", "pH_solo"]
        self.edge_nodes = ["edge_node_1", "edge_node_2", "edge_node_3"]
        self.cloud_connected = True
        
    def read_sensor_data(self):
        """Simulate reading data from farm sensors"""
        data = {}
        for sensor in self.sensors:
            if sensor == "temperatura":
                data[sensor] = round(random.uniform(15.0, 35.0), 2)
            elif sensor == "umidade":
                data[sensor] = round(random.uniform(40.0, 90.0), 2)
            elif sensor == "luminosidade":
                data[sensor] = round(random.uniform(0.0, 100.0), 2)
            elif sensor == "pH_solo":
                data[sensor] = round(random.uniform(5.5, 7.5), 2)
        return data
    
    def process_at_edge(self, data):
        """Simulate edge computing processing"""
        edge_node = random.choice(self.edge_nodes)
        processed_data = {
            "edge_node": edge_node,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "alerts": []
        }
        
        # Check for alerts
        if data["temperatura"] > self.TEMP_HIGH_THRESHOLD:
            processed_data["alerts"].append("Temperatura alta detectada")
        if data["umidade"] < self.HUMIDITY_LOW_THRESHOLD:
            processed_data["alerts"].append("Umidade baixa detectada")
            
        return processed_data
    
    def send_to_cloud(self, processed_data):
        """Simulate sending data to cloud"""
        if self.cloud_connected:
            return True
        return False
    
    def run_simulation(self, duration=120):
        """
        Run the farm simulation for the specified duration
        
        Args:
            duration (int): Duration of simulation in seconds (default: 120)
        """
        print(f"=== Iniciando Simulação de Fazenda Inteligente ===")
        print(f"Duração: {duration} segundos ({duration/60:.1f} minutos)")
        print(f"Sensores: {', '.join(self.sensors)}")
        print(f"Nós Edge: {', '.join(self.edge_nodes)}")
        print(f"Conectividade Cloud: {'Sim' if self.cloud_connected else 'Não'}")
        print("=" * 50)
        
        start_time = time.time()
        iteration = 0
        
        while time.time() - start_time < duration:
            iteration += 1
            elapsed = time.time() - start_time
            
            # Read sensor data
            sensor_data = self.read_sensor_data()
            
            # Process at edge
            processed = self.process_at_edge(sensor_data)
            
            # Send to cloud
            cloud_sent = self.send_to_cloud(processed)
            
            # Display status
            print(f"\n[{elapsed:.1f}s] Iteração {iteration}")
            print(f"  Dados: Temp={sensor_data['temperatura']}°C, "
                  f"Umidade={sensor_data['umidade']}%, "
                  f"Luz={sensor_data['luminosidade']}%, "
                  f"pH={sensor_data['pH_solo']}")
            print(f"  Processado em: {processed['edge_node']}")
            
            if processed['alerts']:
                print(f"  ⚠️  Alertas: {', '.join(processed['alerts'])}")
            
            print(f"  Cloud: {'✓ Enviado' if cloud_sent else '✗ Falha'}")
            
            # Simulate processing interval
            time.sleep(self.ITERATION_INTERVAL)
        
        total_time = time.time() - start_time
        print("\n" + "=" * 50)
        print(f"=== Simulação Concluída ===")
        print(f"Tempo total: {total_time:.1f}s ({total_time/60:.1f} minutos)")
        print(f"Iterações: {iteration}")
        print(f"Taxa média: {iteration/total_time:.2f} iterações/segundo")
        print("=" * 50)


def main():
    """Main entry point with command-line argument parsing"""
    parser = argparse.ArgumentParser(
        description='Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s                    # Executa com duração padrão (120 segundos)
  %(prog)s --duration 600     # Executa por 10 minutos (600 segundos)
  %(prog)s --duration 60      # Executa por 1 minuto (60 segundos)
        """
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=120,
        help='Duração da simulação em segundos (padrão: 120)'
    )
    
    args = parser.parse_args()
    
    # Validate duration
    if args.duration <= 0:
        parser.error("A duração deve ser um número positivo")
    
    # Create and run simulator
    farm_simulator = FarmSimulator()
    farm_simulator.run_simulation(duration=args.duration)


if __name__ == "__main__":
    main()
