#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Simula rede híbrida, edge computing resiliente e testes de validação
"""

import time
import random
import argparse
from datetime import datetime


class EdgeNode:
    """Representa um nó de edge computing na rede"""
    
    def __init__(self, node_id, location):
        self.node_id = node_id
        self.location = location
        self.active = True
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.data_processed = 0
        
    def process_data(self, data_size):
        """Processa dados no nó edge"""
        if self.active:
            self.data_processed += data_size
            self.cpu_usage = min(100.0, random.uniform(20, 80))
            self.memory_usage = min(100.0, random.uniform(30, 70))
            return True
        return False
    
    def get_status(self):
        """Retorna status atual do nó"""
        return {
            'node_id': self.node_id,
            'location': self.location,
            'active': self.active,
            'cpu_usage': f"{self.cpu_usage:.2f}%",
            'memory_usage': f"{self.memory_usage:.2f}%",
            'data_processed': self.data_processed
        }


class CloudServer:
    """Representa servidor cloud central"""
    
    def __init__(self):
        self.total_data_received = 0
        self.requests_processed = 0
        
    def receive_data(self, data_size):
        """Recebe dados dos nós edge"""
        self.total_data_received += data_size
        self.requests_processed += 1
        
    def get_status(self):
        """Retorna status do servidor cloud"""
        return {
            'total_data_received': self.total_data_received,
            'requests_processed': self.requests_processed
        }


class IoTSensor:
    """Representa um sensor IoT no campo agrícola"""
    
    def __init__(self, sensor_id, sensor_type):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.readings_count = 0
        
    def generate_reading(self):
        """Gera uma leitura do sensor"""
        self.readings_count += 1
        # Simula diferentes tipos de dados baseado no tipo de sensor
        if self.sensor_type == 'temperature':
            value = random.uniform(15.0, 35.0)
        elif self.sensor_type == 'humidity':
            value = random.uniform(40.0, 90.0)
        elif self.sensor_type == 'soil_moisture':
            value = random.uniform(20.0, 80.0)
        else:
            value = random.uniform(0.0, 100.0)
            
        return {
            'sensor_id': self.sensor_id,
            'type': self.sensor_type,
            'value': value,
            'timestamp': datetime.now().isoformat()
        }


class AgroEdgeSimulator:
    """Simulador principal da arquitetura híbrida"""
    
    def __init__(self, duration=300):
        self.duration = duration
        self.edge_nodes = []
        self.cloud_server = CloudServer()
        self.iot_sensors = []
        self.start_time = None
        self.running = False
        
    def setup(self):
        """Configura a infraestrutura da simulação"""
        print("=" * 60)
        print("Simulador de Arquitetura Híbrida com Edge Computing")
        print("Para Agricultura Remota")
        print("=" * 60)
        print(f"\nDuração da simulação: {self.duration} segundos (~{self.duration//60} minutos)")
        print("\nConfigurando infraestrutura...")
        
        # Criar nós edge
        locations = ['Fazenda Norte', 'Fazenda Sul', 'Fazenda Leste']
        for i, location in enumerate(locations, 1):
            node = EdgeNode(f"EDGE-{i:02d}", location)
            self.edge_nodes.append(node)
            print(f"  ✓ Nó Edge {node.node_id} criado em {location}")
        
        # Criar sensores IoT
        sensor_types = ['temperature', 'humidity', 'soil_moisture']
        sensor_count = 0
        for node in self.edge_nodes:
            for sensor_type in sensor_types:
                sensor_count += 1
                sensor = IoTSensor(f"SENSOR-{sensor_count:03d}", sensor_type)
                self.iot_sensors.append(sensor)
        
        print(f"  ✓ {len(self.iot_sensors)} sensores IoT criados")
        print(f"  ✓ Servidor Cloud configurado")
        print("\nInfraestrutura pronta!")
        
    def simulate_cycle(self, cycle_num):
        """Executa um ciclo de simulação"""
        # Sensores geram leituras
        for sensor in self.iot_sensors:
            reading = sensor.generate_reading()
            data_size = random.randint(100, 500)  # bytes
            
            # Dados são processados no edge node mais próximo
            edge_node = random.choice(self.edge_nodes)
            if edge_node.process_data(data_size):
                # Ocasionalmente, dados críticos são enviados ao cloud
                if random.random() < 0.3:  # 30% chance
                    self.cloud_server.receive_data(data_size)
        
    def print_status(self, elapsed_time):
        """Imprime status atual da simulação"""
        print(f"\n--- Status da Simulação (t={elapsed_time}s) ---")
        
        # Status dos Edge Nodes
        print("\nNós Edge:")
        for node in self.edge_nodes:
            status = node.get_status()
            print(f"  {status['node_id']} ({status['location']}): "
                  f"CPU={status['cpu_usage']}, "
                  f"MEM={status['memory_usage']}, "
                  f"Dados={status['data_processed']} bytes")
        
        # Status do Cloud
        cloud_status = self.cloud_server.get_status()
        print(f"\nServidor Cloud:")
        print(f"  Dados recebidos: {cloud_status['total_data_received']} bytes")
        print(f"  Requisições processadas: {cloud_status['requests_processed']}")
        
        # Status dos Sensores
        total_readings = sum(s.readings_count for s in self.iot_sensors)
        print(f"\nSensores IoT:")
        print(f"  Total de leituras: {total_readings}")
        
    def run(self):
        """Executa a simulação"""
        self.setup()
        
        print(f"\nIniciando simulação às {datetime.now().strftime('%H:%M:%S')}...")
        print("Pressione Ctrl+C para interromper\n")
        
        self.start_time = time.time()
        self.running = True
        cycle_num = 0
        last_status_time = 0
        
        try:
            while self.running:
                current_time = time.time()
                elapsed_time = int(current_time - self.start_time)
                
                # Verifica se atingiu a duração
                if elapsed_time >= self.duration:
                    break
                
                # Executa ciclo de simulação
                cycle_num += 1
                self.simulate_cycle(cycle_num)
                
                # Imprime status a cada 30 segundos
                if elapsed_time - last_status_time >= 30:
                    self.print_status(elapsed_time)
                    last_status_time = elapsed_time
                
                # Aguarda antes do próximo ciclo (simula taxa de amostragem)
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nSimulação interrompida pelo usuário!")
        
        finally:
            self.finalize()
    
    def finalize(self):
        """Finaliza a simulação e mostra resultados"""
        end_time = time.time()
        total_time = int(end_time - self.start_time)
        
        print("\n" + "=" * 60)
        print("SIMULAÇÃO FINALIZADA")
        print("=" * 60)
        print(f"\nTempo total de execução: {total_time} segundos")
        
        self.print_status(total_time)
        
        # Estatísticas finais
        print("\n" + "=" * 60)
        print("RESUMO FINAL")
        print("=" * 60)
        
        total_edge_data = sum(node.data_processed for node in self.edge_nodes)
        cloud_status = self.cloud_server.get_status()
        total_readings = sum(s.readings_count for s in self.iot_sensors)
        
        print(f"Total de dados processados nos Edge Nodes: {total_edge_data} bytes")
        print(f"Total de dados enviados ao Cloud: {cloud_status['total_data_received']} bytes")
        print(f"Total de leituras dos sensores: {total_readings}")
        print(f"Eficiência do Edge Computing: {(total_edge_data / (total_edge_data + cloud_status['total_data_received']) * 100):.2f}%")
        print("\nSimulação concluída com sucesso!")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=300,
        help='Duração da simulação em segundos (padrão: 300 segundos ≈ 5 minutos)'
    )
    
    args = parser.parse_args()
    
    # Valida duração
    if args.duration <= 0:
        print("Erro: A duração deve ser maior que 0")
        return 1
    
    # Cria e executa simulador
    simulator = AgroEdgeSimulator(duration=args.duration)
    simulator.run()
    
    return 0


if __name__ == "__main__":
    exit(main())
