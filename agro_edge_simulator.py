#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Simula rede híbrida, edge computing resiliente e testes de validação
"""

import argparse
import time
import random
import sys
from datetime import datetime

# Alert thresholds for different sensor types
TEMP_HIGH_THRESHOLD = 32.0
TEMP_LOW_THRESHOLD = 18.0
HUMIDITY_LOW_THRESHOLD = 40.0
SOIL_LOW_THRESHOLD = 30.0


class SensorNode:
    """Representa um nó sensor na rede agrícola"""
    
    def __init__(self, node_id, sensor_type):
        self.node_id = node_id
        self.sensor_type = sensor_type
        self.data_points = 0
    
    def collect_data(self):
        """Simula coleta de dados do sensor"""
        self.data_points += 1
        if self.sensor_type == "temperatura":
            return {"type": self.sensor_type, "value": round(random.uniform(15.0, 35.0), 2)}
        elif self.sensor_type == "umidade":
            return {"type": self.sensor_type, "value": round(random.uniform(30.0, 90.0), 2)}
        elif self.sensor_type == "solo":
            return {"type": self.sensor_type, "value": round(random.uniform(20.0, 80.0), 2)}
        return {"type": "unknown", "value": 0}


class EdgeNode:
    """Representa um nó de edge computing"""
    
    def __init__(self, edge_id):
        self.edge_id = edge_id
        self.processed_data = 0
        self.alerts_generated = 0
    
    def process_data(self, sensor_data):
        """Processa dados no edge node"""
        self.processed_data += 1
        
        # Gera alertas baseado em condições críticas
        if sensor_data["type"] == "temperatura" and (sensor_data["value"] > TEMP_HIGH_THRESHOLD or sensor_data["value"] < TEMP_LOW_THRESHOLD):
            self.alerts_generated += 1
            return True
        elif sensor_data["type"] == "umidade" and sensor_data["value"] < HUMIDITY_LOW_THRESHOLD:
            self.alerts_generated += 1
            return True
        elif sensor_data["type"] == "solo" and sensor_data["value"] < SOIL_LOW_THRESHOLD:
            self.alerts_generated += 1
            return True
        return False


class CloudNode:
    """Representa o nó na nuvem para processamento centralizado"""
    
    def __init__(self):
        self.total_data_received = 0
        self.alerts_processed = 0
    
    def receive_data(self, data_count):
        """Recebe dados agregados do edge"""
        self.total_data_received += data_count
    
    def process_alert(self):
        """Processa alertas recebidos"""
        self.alerts_processed += 1


class AgroEdgeSimulator:
    """Simulador principal da arquitetura híbrida"""
    
    def __init__(self, duration):
        self.duration = duration
        self.sensors = []
        self.edge_nodes = []
        self.cloud = CloudNode()
        self.start_time = None
        self.end_time = None
        self.last_cloud_sync_data_count = 0
        
        # Inicializa a topologia da rede
        self._initialize_network()
    
    def _initialize_network(self):
        """Inicializa a topologia da rede agrícola"""
        # Cria sensores
        sensor_types = ["temperatura", "umidade", "solo"]
        for i in range(9):
            sensor_type = sensor_types[i % 3]
            self.sensors.append(SensorNode(f"S{i+1}", sensor_type))
        
        # Cria edge nodes
        for i in range(3):
            self.edge_nodes.append(EdgeNode(f"E{i+1}"))
    
    def run_simulation(self):
        """Executa a simulação por um período especificado"""
        print("=" * 80)
        print("Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto")
        print("=" * 80)
        print(f"Duração da simulação: {self.duration} segundos ({self.duration / 60:.1f} minutos)")
        print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Topologia: {len(self.sensors)} sensores, {len(self.edge_nodes)} edge nodes, 1 cloud node")
        print("=" * 80)
        print()
        
        self.start_time = time.time()
        iteration = 0
        
        try:
            while True:
                elapsed = time.time() - self.start_time
                if elapsed >= self.duration:
                    break
                
                iteration += 1
                
                # Cada sensor coleta dados
                for i, sensor in enumerate(self.sensors):
                    data = sensor.collect_data()
                    
                    # Distribui sensores entre edge nodes
                    edge_node = self.edge_nodes[i % len(self.edge_nodes)]
                    
                    # Edge node processa os dados
                    alert_generated = edge_node.process_data(data)
                    
                    if alert_generated:
                        self.cloud.process_alert()
                
                # Envia dados agregados para a nuvem periodicamente
                if iteration % 10 == 0:
                    total_data = sum(sensor.data_points for sensor in self.sensors)
                    new_data = total_data - self.last_cloud_sync_data_count
                    self.cloud.receive_data(new_data)
                    self.last_cloud_sync_data_count = total_data
                
                # Exibe progresso a cada 10% do tempo
                progress_percent = (elapsed / self.duration) * 100
                if iteration == 1 or int(progress_percent) % 10 == 0 and int((elapsed - 1) / self.duration * 100) % 10 != 0:
                    self._print_status(elapsed, iteration)
                
                # Simula intervalo de coleta de dados (1 segundo)
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\nSimulação interrompida pelo usuário!")
            elapsed = time.time() - self.start_time
        
        self.end_time = time.time()
        self._print_summary(elapsed)
    
    def _print_status(self, elapsed, iteration):
        """Imprime status atual da simulação"""
        progress = (elapsed / self.duration) * 100
        remaining = self.duration - elapsed
        
        total_alerts = sum(edge.alerts_generated for edge in self.edge_nodes)
        total_processed = sum(edge.processed_data for edge in self.edge_nodes)
        
        print(f"[{progress:5.1f}%] Iteração {iteration:4d} | "
              f"Tempo decorrido: {int(elapsed):4d}s | "
              f"Restante: {int(remaining):4d}s | "
              f"Dados processados: {total_processed:5d} | "
              f"Alertas: {total_alerts:3d}")
    
    def _print_summary(self, actual_duration):
        """Imprime resumo final da simulação"""
        print()
        print("=" * 80)
        print("RESUMO DA SIMULAÇÃO")
        print("=" * 80)
        print(f"Duração real: {actual_duration:.2f} segundos ({actual_duration / 60:.2f} minutos)")
        print(f"Término: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("Estatísticas dos Sensores:")
        print("-" * 80)
        for sensor in self.sensors:
            print(f"  {sensor.node_id} ({sensor.sensor_type:12s}): {sensor.data_points:5d} leituras")
        
        total_data_points = sum(sensor.data_points for sensor in self.sensors)
        print(f"\nTotal de leituras: {total_data_points}")
        print()
        
        print("Estatísticas dos Edge Nodes:")
        print("-" * 80)
        for edge in self.edge_nodes:
            print(f"  {edge.edge_id}: {edge.processed_data:5d} dados processados, "
                  f"{edge.alerts_generated:3d} alertas gerados")
        
        total_processed = sum(edge.processed_data for edge in self.edge_nodes)
        total_alerts = sum(edge.alerts_generated for edge in self.edge_nodes)
        print(f"\nTotal processado no edge: {total_processed}")
        print(f"Total de alertas gerados: {total_alerts}")
        print()
        
        print("Estatísticas do Cloud Node:")
        print("-" * 80)
        print(f"  Dados recebidos: {self.cloud.total_data_received}")
        print(f"  Alertas processados: {self.cloud.alerts_processed}")
        print()
        
        print("=" * 80)
        print("Simulação concluída com sucesso!")
        print("=" * 80)


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s --duration 600        # Executa simulação por 10 minutos
  %(prog)s --duration 1800       # Executa simulação por 30 minutos
        """
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        required=True,
        help="Duração da simulação em segundos (ex: 600 para 10 minutos, 1800 para 30 minutos)"
    )
    
    args = parser.parse_args()
    
    # Valida o argumento duration
    if args.duration <= 0:
        print("Erro: A duração deve ser um número positivo.", file=sys.stderr)
        sys.exit(1)
    
    # Cria e executa o simulador
    simulator = AgroEdgeSimulator(args.duration)
    simulator.run_simulation()


if __name__ == "__main__":
    main()
