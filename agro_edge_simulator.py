#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Simula rede híbrida, edge computing resiliente e testes de validação
"""

import time
import random
import argparse
import logging
from datetime import datetime

# Constantes de configuração
STATUS_REPORT_INTERVAL_SECONDS = 30
SAMPLING_INTERVAL_SECONDS = 1
CLOUD_FORWARD_RATIO = 0.2  # 20% dos dados enviados ao cloud
MAX_DURATION_SECONDS = 86400  # 24 horas


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
            # Atualiza uso de CPU e memória com base na carga e no histórico
            load_factor = min(1.0, max(0.0, data_size / 1000.0))
            
            # CPU tende a aumentar com a carga atual, variando gradualmente
            cpu_delta = load_factor * 10.0 + random.uniform(-2.0, 4.0)
            self.cpu_usage = max(0.0, min(100.0, self.cpu_usage + cpu_delta))
            
            # Memória tem inércia maior: leve decaimento + aumento com a carga
            memory_base = self.memory_usage * 0.95
            memory_delta = load_factor * 5.0 + random.uniform(-1.0, 3.0)
            self.memory_usage = max(0.0, min(100.0, memory_base + memory_delta))
            
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
    
    def __init__(self, duration=300, num_edges=3, sensors_per_edge=3, cloud_forward_ratio=CLOUD_FORWARD_RATIO):
        self.duration = duration
        self.num_edges = num_edges
        self.sensors_per_edge = sensors_per_edge
        self.cloud_forward_ratio = cloud_forward_ratio
        self.edge_nodes = []
        self.cloud_server = CloudServer()
        self.iot_sensors = []
        self.sensor_to_edge_map = {}  # Mapeamento sensor -> edge node
        self.start_time = None
        self.running = False
        
    def _estimate_data_size(self, sensor):
        """
        Estima o tamanho do payload (em bytes) de uma leitura de sensor,
        levando em conta o tipo de sensor.
        """
        sensor_type = sensor.sensor_type
        
        if sensor_type == 'temperature':
            # Leituras de temperatura tendem a ser simples (valor + timestamp)
            return random.randint(80, 180)
        elif sensor_type == 'humidity':
            # Um pouco mais de metadados que temperatura
            return random.randint(120, 220)
        elif sensor_type == 'soil_moisture':
            # Pode incluir múltiplos parâmetros (umidade, condutividade etc.)
            return random.randint(180, 320)
        
        # Fallback para tipos desconhecidos
        return random.randint(100, 500)
        
    def setup(self):
        """Configura a infraestrutura da simulação"""
        print("=" * 60)
        print("Simulador de Arquitetura Híbrida com Edge Computing")
        print("Para Agricultura Remota")
        print("=" * 60)
        print(f"\nDuração da simulação: {self.duration} segundos (~{self.duration//60} minutos)")
        print(f"Nós Edge: {self.num_edges}")
        print(f"Sensores por nó: {self.sensors_per_edge}")
        print(f"Taxa de envio ao Cloud: {self.cloud_forward_ratio*100:.0f}%")
        print("\nConfigurando infraestrutura...")
        
        # Criar nós edge
        locations = ['Fazenda Norte', 'Fazenda Sul', 'Fazenda Leste', 'Fazenda Oeste', 'Fazenda Centro']
        for i in range(self.num_edges):
            location = locations[i % len(locations)]
            node = EdgeNode(f"EDGE-{i+1:02d}", location)
            self.edge_nodes.append(node)
            logging.info(f"Nó Edge {node.node_id} criado em {location}")
            print(f"  ✓ Nó Edge {node.node_id} criado em {location}")
        
        # Criar sensores IoT e mapear para edge nodes
        sensor_types = ['temperature', 'humidity', 'soil_moisture']
        sensor_count = 0
        for edge_idx, edge_node in enumerate(self.edge_nodes):
            for _ in range(self.sensors_per_edge):
                sensor_count += 1
                sensor_type = sensor_types[sensor_count % len(sensor_types)]
                sensor = IoTSensor(f"SENSOR-{sensor_count:03d}", sensor_type)
                self.iot_sensors.append(sensor)
                # Mapeia sensor ao edge node baseado em proximidade geográfica
                self.sensor_to_edge_map[sensor.sensor_id] = edge_node
        
        print(f"  ✓ {len(self.iot_sensors)} sensores IoT criados")
        print(f"  ✓ Servidor Cloud configurado")
        print("\nInfraestrutura pronta!")
        
    def simulate_cycle(self):
        """Executa um ciclo de simulação"""
        # Sensores geram leituras
        for sensor in self.iot_sensors:
            sensor.generate_reading()
            data_size = self._estimate_data_size(sensor)
            
            # Obtém edge node baseado em proximidade geográfica
            edge_node = self.sensor_to_edge_map[sensor.sensor_id]
            
            # Decide se dados vão para edge ou cloud (não ambos)
            if random.random() < self.cloud_forward_ratio:
                # Dados críticos são enviados diretamente ao cloud
                self.cloud_server.receive_data(data_size)
                logging.debug(f"Sensor {sensor.sensor_id} enviou dados ao cloud")
            else:
                # Dados são processados localmente no edge
                if edge_node.process_data(data_size):
                    logging.debug(f"Sensor {sensor.sensor_id} processou dados no {edge_node.node_id}")
                else:
                    # Fallback: se edge falhar, envia ao cloud
                    self.cloud_server.receive_data(data_size)
                    logging.warning(f"Edge node {edge_node.node_id} inativo, dados enviados ao cloud")
        
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
        last_status_time = 0
        
        try:
            while self.running:
                current_time = time.time()
                elapsed_time = int(current_time - self.start_time)
                
                # Verifica se atingiu a duração
                if elapsed_time >= self.duration:
                    break
                
                # Executa ciclo de simulação
                self.simulate_cycle()
                
                # Imprime status a cada intervalo definido
                if elapsed_time - last_status_time >= STATUS_REPORT_INTERVAL_SECONDS:
                    self.print_status(elapsed_time)
                    last_status_time = elapsed_time
                
                # Aguarda antes do próximo ciclo (simula taxa de amostragem)
                time.sleep(SAMPLING_INTERVAL_SECONDS)
                
        except KeyboardInterrupt:
            print("\n\nSimulação interrompida pelo usuário!")
        
        finally:
            self.finalize()
    
    def finalize(self):
        """Finaliza a simulação e mostra resultados"""
        end_time = time.time()
        total_time = int(end_time - self.start_time) if self.start_time else 0
        
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
        
        # Calcula eficiência do Edge Computing (evita divisão por zero)
        total_data = total_edge_data + cloud_status['total_data_received']
        if total_data > 0:
            efficiency = (total_edge_data / total_data) * 100
            print(f"Eficiência do Edge Computing: {efficiency:.2f}%")
        else:
            print("Eficiência do Edge Computing: N/A (sem dados processados)")
        
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
    parser.add_argument(
        '--num-edges',
        type=int,
        default=3,
        help='Número de nós edge (padrão: 3)'
    )
    parser.add_argument(
        '--sensors-per-edge',
        type=int,
        default=3,
        help='Sensores IoT por nó edge (padrão: 3)'
    )
    parser.add_argument(
        '--cloud-forward-ratio',
        type=float,
        default=CLOUD_FORWARD_RATIO,
        help=f'Fração de dados enviados ao cloud, entre 0 e 1 (padrão: {CLOUD_FORWARD_RATIO})'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='WARNING',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Nível de log (padrão: WARNING)'
    )
    
    args = parser.parse_args()
    
    # Configura logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Valida parâmetros
    try:
        if args.duration <= 0:
            raise ValueError("A duração deve ser maior que 0")
        if args.duration > MAX_DURATION_SECONDS:
            raise ValueError(f"A duração não pode exceder {MAX_DURATION_SECONDS} segundos (24 horas)")
        if args.num_edges <= 0:
            raise ValueError("O número de nós edge deve ser maior que 0")
        if args.sensors_per_edge <= 0:
            raise ValueError("O número de sensores por edge deve ser maior que 0")
        if not 0 <= args.cloud_forward_ratio <= 1:
            raise ValueError("A taxa de envio ao cloud deve estar entre 0 e 1")
    except ValueError as e:
        print(f"Erro de validação: {e}")
        return 1
    
    # Cria e executa simulador
    simulator = AgroEdgeSimulator(
        duration=args.duration,
        num_edges=args.num_edges,
        sensors_per_edge=args.sensors_per_edge,
        cloud_forward_ratio=args.cloud_forward_ratio
    )
    simulator.run()
    
    return 0


if __name__ == "__main__":
    exit(main())
