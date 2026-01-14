#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Simulator of Hybrid Architecture with Edge Computing for Remote Agriculture

Este simulador implementa uma rede híbrida que combina edge computing e cloud computing
para cenários de agricultura remota, com foco em resiliência e eficiência.
"""

import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import json


class NodeType(Enum):
    """Tipos de nós na rede"""
    SENSOR = "sensor"
    EDGE = "edge"
    CLOUD = "cloud"
    GATEWAY = "gateway"


class DataPriority(Enum):
    """Prioridade dos dados"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class SensorData:
    """Dados coletados pelos sensores"""
    sensor_id: str
    timestamp: float
    data_type: str
    value: float
    priority: DataPriority
    processed: bool = False
    location: str = ""
    
    def to_dict(self) -> dict:
        return {
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp,
            'data_type': self.data_type,
            'value': self.value,
            'priority': self.priority.name,
            'processed': self.processed,
            'location': self.location
        }


@dataclass
class Node:
    """Representa um nó na rede"""
    node_id: str
    node_type: NodeType
    location: str
    capacity: int
    status: str = "active"
    connected_nodes: List[str] = field(default_factory=list)
    data_queue: List[SensorData] = field(default_factory=list)
    processed_count: int = 0
    latency_ms: float = 0.0
    
    def process_data(self, data: SensorData) -> bool:
        """Processa dados no nó"""
        if len(self.data_queue) < self.capacity and self.status == "active":
            self.data_queue.append(data)
            data.processed = True
            self.processed_count += 1
            return True
        return False
    
    def get_status(self) -> dict:
        return {
            'node_id': self.node_id,
            'type': self.node_type.value,
            'location': self.location,
            'status': self.status,
            'queue_size': len(self.data_queue),
            'capacity': self.capacity,
            'processed_count': self.processed_count,
            'latency_ms': self.latency_ms
        }


class EdgeComputingSimulator:
    """Simulador principal de Edge Computing para Agricultura"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()
        self.nodes: Dict[str, Node] = {}
        self.sensors: List[str] = []
        self.edge_nodes: List[str] = []
        self.cloud_nodes: List[str] = []
        self.gateway_nodes: List[str] = []
        self.total_data_generated = 0
        self.total_data_processed = 0
        self.simulation_time = 0.0
        self.metrics: Dict = {
            'latency': []
        }
        
    def _default_config(self) -> Dict:
        """Configuração padrão do simulador"""
        return {
            'num_sensors': 10,
            'num_edge_nodes': 3,
            'num_cloud_nodes': 1,
            'num_gateway_nodes': 2,
            'edge_capacity': 100,
            'cloud_capacity': 1000,
            'gateway_capacity': 50,
            'simulation_duration': 60,
            'data_generation_rate': 1.0
        }
    
    def initialize_network(self):
        """Inicializa a topologia da rede"""
        print("Inicializando rede híbrida...")
        
        # Criar sensores
        for i in range(self.config['num_sensors']):
            sensor_id = f"sensor_{i}"
            location = f"field_{i % 3}"  # Distribui sensores em 3 campos
            sensor = Node(
                node_id=sensor_id,
                node_type=NodeType.SENSOR,
                location=location,
                capacity=10
            )
            self.nodes[sensor_id] = sensor
            self.sensors.append(sensor_id)
        
        # Criar nós Edge
        for i in range(self.config['num_edge_nodes']):
            edge_id = f"edge_{i}"
            location = f"field_{i}"
            edge = Node(
                node_id=edge_id,
                node_type=NodeType.EDGE,
                location=location,
                capacity=self.config['edge_capacity'],
                latency_ms=random.uniform(5, 15)
            )
            self.nodes[edge_id] = edge
            self.edge_nodes.append(edge_id)
        
        # Criar Gateways
        for i in range(self.config['num_gateway_nodes']):
            gateway_id = f"gateway_{i}"
            gateway = Node(
                node_id=gateway_id,
                node_type=NodeType.GATEWAY,
                location="central",
                capacity=self.config['gateway_capacity'],
                latency_ms=random.uniform(15, 30)
            )
            self.nodes[gateway_id] = gateway
            self.gateway_nodes.append(gateway_id)
        
        # Criar nós Cloud
        for i in range(self.config['num_cloud_nodes']):
            cloud_id = f"cloud_{i}"
            cloud = Node(
                node_id=cloud_id,
                node_type=NodeType.CLOUD,
                location="remote_datacenter",
                capacity=self.config['cloud_capacity'],
                latency_ms=random.uniform(50, 100)
            )
            self.nodes[cloud_id] = cloud
            self.cloud_nodes.append(cloud_id)
        
        # Estabelecer conexões
        self._setup_connections()
        
        print(f"Rede inicializada com {len(self.sensors)} sensores, "
              f"{len(self.edge_nodes)} edge nodes, {len(self.gateway_nodes)} gateways, "
              f"e {len(self.cloud_nodes)} cloud nodes")
    
    def _setup_connections(self):
        """Estabelece conexões entre os nós"""
        # Conectar sensores aos edge nodes (distribuição baseada em localização)
        for sensor_id in self.sensors:
            sensor = self.nodes[sensor_id]
            # Encontrar edge node na mesma localização
            connected = False
            for edge_id in self.edge_nodes:
                edge = self.nodes[edge_id]
                if edge.location == sensor.location:
                    sensor.connected_nodes.append(edge_id)
                    edge.connected_nodes.append(sensor_id)
                    connected = True
                    break
            
            # Se não encontrar edge node na mesma localização, conectar ao mais próximo
            if not connected and self.edge_nodes:
                nearest_edge_id = self.edge_nodes[0]
                sensor.connected_nodes.append(nearest_edge_id)
                self.nodes[nearest_edge_id].connected_nodes.append(sensor_id)
        
        # Conectar edge nodes aos gateways
        for edge_id in self.edge_nodes:
            edge = self.nodes[edge_id]
            for gateway_id in self.gateway_nodes:
                edge.connected_nodes.append(gateway_id)
                self.nodes[gateway_id].connected_nodes.append(edge_id)
        
        # Conectar gateways à cloud
        for gateway_id in self.gateway_nodes:
            gateway = self.nodes[gateway_id]
            for cloud_id in self.cloud_nodes:
                gateway.connected_nodes.append(cloud_id)
                self.nodes[cloud_id].connected_nodes.append(gateway_id)
    
    def generate_sensor_data(self) -> SensorData:
        """Gera dados de sensor simulados"""
        if not self.sensors:
            raise ValueError("Nenhum sensor disponível para gerar dados")
        
        sensor_id = random.choice(self.sensors)
        sensor = self.nodes[sensor_id]
        
        # Tipos de dados agrícolas
        data_types = [
            ('soil_moisture', 0, 100, DataPriority.MEDIUM),
            ('temperature', -10, 50, DataPriority.LOW),
            ('humidity', 0, 100, DataPriority.LOW),
            ('soil_ph', 0, 14, DataPriority.MEDIUM),
            ('pest_detection', 0, 1, DataPriority.HIGH),
            ('irrigation_alert', 0, 1, DataPriority.CRITICAL)
        ]
        
        data_type, min_val, max_val, priority = random.choice(data_types)
        
        return SensorData(
            sensor_id=sensor_id,
            timestamp=time.time(),
            data_type=data_type,
            value=random.uniform(min_val, max_val),
            priority=priority,
            location=sensor.location
        )
    
    def route_data(self, data: SensorData) -> bool:
        """Roteia dados através da rede híbrida com lógica de resiliência"""
        sensor = self.nodes[data.sensor_id]
        
        # Estratégia 1: Processar localmente no Edge (prioridade para dados críticos)
        if data.priority in [DataPriority.CRITICAL, DataPriority.HIGH]:
            # Tentar processar no edge node local
            for edge_id in sensor.connected_nodes:
                edge = self.nodes[edge_id]
                if edge.node_type == NodeType.EDGE and edge.status == "active":
                    if edge.process_data(data):
                        self.metrics['latency'].append(edge.latency_ms)
                        return True
        
        # Estratégia 2: Usar gateway para dados de prioridade média
        if data.priority == DataPriority.MEDIUM:
            # Tentar primeiro edge, depois gateway
            for edge_id in sensor.connected_nodes:
                edge = self.nodes[edge_id]
                if edge.node_type == NodeType.EDGE:
                    for gateway_id in edge.connected_nodes:
                        gateway = self.nodes[gateway_id]
                        if gateway.node_type == NodeType.GATEWAY and gateway.status == "active":
                            if gateway.process_data(data):
                                self.metrics['latency'].append(gateway.latency_ms)
                                return True
        
        # Estratégia 3: Cloud para processamento em batch (dados de baixa prioridade)
        for edge_id in sensor.connected_nodes:
            edge = self.nodes[edge_id]
            if edge.node_type == NodeType.EDGE:
                for gateway_id in edge.connected_nodes:
                    gateway = self.nodes[gateway_id]
                    if gateway.node_type == NodeType.GATEWAY:
                        for cloud_id in gateway.connected_nodes:
                            cloud = self.nodes[cloud_id]
                            if cloud.node_type == NodeType.CLOUD and cloud.status == "active":
                                if cloud.process_data(data):
                                    self.metrics['latency'].append(cloud.latency_ms)
                                    return True
        
        return False
    
    def simulate_failure(self):
        """Simula falha de nó para testar resiliência"""
        eligible_nodes = self.edge_nodes + self.gateway_nodes
        if not eligible_nodes:
            return
            
        if random.random() < 0.1:  # 10% de chance de falha
            node_id = random.choice(eligible_nodes)
            node = self.nodes[node_id]
            if node.status == "active":
                node.status = "failed"
                print(f"⚠️  Falha simulada no nó {node_id}")
        
        # Auto-recuperação de nós falhos (em ciclo separado)
        for node_id in eligible_nodes:
            node = self.nodes[node_id]
            if node.status == "failed" and random.random() < 0.3:  # 30% de chance de recuperação
                node.status = "active"
                print(f"✅ Nó {node_id} recuperado")
    
    def run_simulation(self):
        """Executa a simulação completa"""
        print("\n" + "="*60)
        print("INICIANDO SIMULAÇÃO DE EDGE COMPUTING PARA AGRO REMOTO")
        print("="*60 + "\n")
        
        self.initialize_network()
        
        duration = self.config['simulation_duration']
        rate = self.config['data_generation_rate']
        
        print(f"\nExecutando simulação por {duration} segundos...")
        print(f"Taxa de geração de dados: {rate} dados/segundo\n")
        
        start_time = time.time()
        cycle = 0
        
        while (time.time() - start_time) < duration:
            cycle += 1
            
            # Gerar e processar dados
            data = self.generate_sensor_data()
            self.total_data_generated += 1
            
            if self.route_data(data):
                self.total_data_processed += 1
            
            # Simular falhas ocasionais
            if cycle % 10 == 0:
                self.simulate_failure()
            
            # Exibir progresso
            if cycle % 20 == 0:
                elapsed = time.time() - start_time
                print(f"Ciclo {cycle} | Tempo: {elapsed:.1f}s | "
                      f"Dados gerados: {self.total_data_generated} | "
                      f"Processados: {self.total_data_processed}")
            
            time.sleep(1.0 / rate)
        
        self.simulation_time = time.time() - start_time
        self._generate_report()
    
    def _generate_report(self):
        """Gera relatório final da simulação"""
        print("\n" + "="*60)
        print("RELATÓRIO DA SIMULAÇÃO")
        print("="*60 + "\n")
        
        print(f"Duração da simulação: {self.simulation_time:.2f} segundos")
        print(f"Total de dados gerados: {self.total_data_generated}")
        print(f"Total de dados processados: {self.total_data_processed}")
        
        success_rate = (self.total_data_processed / self.total_data_generated * 100) if self.total_data_generated > 0 else 0
        print(f"Taxa de sucesso: {success_rate:.2f}%")
        
        if self.metrics['latency']:
            avg_latency = sum(self.metrics['latency']) / len(self.metrics['latency'])
            print(f"Latência média: {avg_latency:.2f}ms")
        
        print("\n--- Status dos Nós ---")
        for node_type in [NodeType.EDGE, NodeType.GATEWAY, NodeType.CLOUD]:
            nodes_of_type = [n for n in self.nodes.values() if n.node_type == node_type]
            if nodes_of_type:
                print(f"\n{node_type.value.upper()}:")
                for node in nodes_of_type:
                    status = node.get_status()
                    print(f"  {status['node_id']}: "
                          f"Status={status['status']}, "
                          f"Processados={status['processed_count']}, "
                          f"Fila={status['queue_size']}/{status['capacity']}")
        
        print("\n" + "="*60)
        print("TESTES DE VALIDAÇÃO")
        print("="*60 + "\n")
        
        self._run_validation_tests()
    
    def _run_validation_tests(self):
        """Executa testes de validação"""
        tests_passed = 0
        tests_total = 0
        
        # Teste 1: Verificar se há nós ativos
        tests_total += 1
        active_nodes = [n for n in self.nodes.values() if n.status == "active"]
        if len(active_nodes) > 0:
            print("✅ Teste 1: Existem nós ativos na rede")
            tests_passed += 1
        else:
            print("❌ Teste 1: Nenhum nó ativo encontrado")
        
        # Teste 2: Verificar processamento de dados
        tests_total += 1
        if self.total_data_processed > 0:
            print("✅ Teste 2: Dados foram processados com sucesso")
            tests_passed += 1
        else:
            print("❌ Teste 2: Nenhum dado foi processado")
        
        # Teste 3: Verificar edge computing
        tests_total += 1
        edge_processed = sum(n.processed_count for n in self.nodes.values() if n.node_type == NodeType.EDGE)
        if edge_processed > 0:
            print("✅ Teste 3: Edge nodes processaram dados localmente")
            tests_passed += 1
        else:
            print("❌ Teste 3: Edge nodes não processaram dados")
        
        # Teste 4: Verificar resiliência (cloud backup)
        tests_total += 1
        cloud_processed = sum(n.processed_count for n in self.nodes.values() if n.node_type == NodeType.CLOUD)
        if cloud_processed > 0 or edge_processed > 0:
            print("✅ Teste 4: Sistema demonstrou resiliência (processamento distribuído)")
            tests_passed += 1
        else:
            print("❌ Teste 4: Sistema não demonstrou resiliência")
        
        # Teste 5: Verificar latência
        tests_total += 1
        if self.metrics['latency'] and max(self.metrics['latency']) < 200:
            print("✅ Teste 5: Latência dentro de limites aceitáveis (<200ms)")
            tests_passed += 1
        else:
            print("❌ Teste 5: Latência excedeu limites")
        
        print(f"\nResultado: {tests_passed}/{tests_total} testes aprovados")
        
        if tests_passed == tests_total:
            print("🎉 Todos os testes de validação passaram!")
        elif tests_passed >= tests_total * 0.8:
            print("⚠️  Maioria dos testes passou, mas há melhorias necessárias")
        else:
            print("❌ Muitos testes falharam, revisar configuração")
    
    def export_results(self, filename: str = "simulation_results.json"):
        """Exporta resultados da simulação para arquivo JSON"""
        results = {
            'config': self.config,
            'summary': {
                'simulation_time': self.simulation_time,
                'total_data_generated': self.total_data_generated,
                'total_data_processed': self.total_data_processed,
                'success_rate': (self.total_data_processed / self.total_data_generated * 100) 
                                if self.total_data_generated > 0 else 0
            },
            'metrics': {
                'avg_latency': sum(self.metrics['latency']) / len(self.metrics['latency']) 
                              if self.metrics['latency'] else 0,
                'latency_samples': len(self.metrics['latency'])
            },
            'nodes': {node_id: node.get_status() for node_id, node in self.nodes.items()}
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Resultados exportados para {filename}")


def main():
    """Função principal para execução do simulador"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║  SIMULADOR DE ARQUITETURA HÍBRIDA COM EDGE COMPUTING        ║
    ║  PARA AGRICULTURA REMOTA                                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Configuração personalizada (opcional)
    custom_config = {
        'num_sensors': 10,
        'num_edge_nodes': 3,
        'num_cloud_nodes': 1,
        'num_gateway_nodes': 2,
        'edge_capacity': 100,
        'cloud_capacity': 1000,
        'gateway_capacity': 50,
        'simulation_duration': 30,  # segundos
        'data_generation_rate': 2.0  # dados por segundo
    }
    
    # Criar e executar simulador
    simulator = EdgeComputingSimulator(config=custom_config)
    simulator.run_simulation()
    
    # Exportar resultados
    simulator.export_results()
    
    print("\n✅ Simulação concluída com sucesso!")
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
