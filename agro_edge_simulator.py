#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
(Hybrid Architecture Simulator with Edge Computing for Remote Agriculture)

Simula rede híbrida, edge computing resiliente e testes de validação
"""

import random
import time
from datetime import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum


# Configurações de simulação
EDGE_FAILURE_PROBABILITY = 0.1  # 10% de chance de falha em cada ciclo

# Faixas de valores para sensores
SENSOR_VALUE_RANGES = {
    "TEMPERATURA": (15.0, 32.0),
    "UMIDADE_SOLO": (25.0, 85.0),
    "UMIDADE_AR": (40.0, 90.0),
    "LUZ": (0.0, 100.0),
    "PH_SOLO": (5.5, 7.5),
    "PRECIPITACAO": (0.0, 50.0)
}

# Thresholds de alerta
ALERT_THRESHOLDS = {
    "TEMPERATURA_MIN": 10,
    "TEMPERATURA_MAX": 35,
    "UMIDADE_SOLO_MIN": 30
}


class SensorType(Enum):
    """Tipos de sensores agrícolas"""
    TEMPERATURA = "Temperatura"
    UMIDADE_SOLO = "Umidade do Solo"
    UMIDADE_AR = "Umidade do Ar"
    LUZ = "Luminosidade"
    PH_SOLO = "pH do Solo"
    PRECIPITACAO = "Precipitação"


class ProcessingLayer(Enum):
    """Camadas de processamento"""
    SENSOR = "Sensor"
    EDGE = "Edge"
    CLOUD = "Cloud"


@dataclass
class SensorData:
    """Dados coletados de um sensor"""
    sensor_id: str
    sensor_type: SensorType
    value: float
    timestamp: datetime
    location: Tuple[float, float]  # (latitude, longitude)
    
    def __str__(self):
        return f"{self.sensor_type.value}: {self.value:.2f} ({self.sensor_id} @ {self.timestamp.strftime('%H:%M:%S')})"


@dataclass
class EdgeNode:
    """Nó de Edge Computing"""
    node_id: str
    location: Tuple[float, float]
    processing_capacity: float  # MIPS
    storage_capacity: float  # MB
    connected_sensors: List[str] = field(default_factory=list)
    data_buffer: List[SensorData] = field(default_factory=list)
    processed_data: int = 0
    is_online: bool = True
    
    def process_data(self, data: SensorData) -> Dict:
        """Processa dados localmente no edge"""
        if not self.is_online:
            return {"status": "offline", "layer": ProcessingLayer.EDGE}
        
        self.data_buffer.append(data)
        self.processed_data += 1
        
        # Análise simples no edge
        alert = False
        if data.sensor_type == SensorType.TEMPERATURA and (
            data.value < ALERT_THRESHOLDS["TEMPERATURA_MIN"] or 
            data.value > ALERT_THRESHOLDS["TEMPERATURA_MAX"]
        ):
            alert = True
        elif data.sensor_type == SensorType.UMIDADE_SOLO and data.value < ALERT_THRESHOLDS["UMIDADE_SOLO_MIN"]:
            alert = True
        
        return {
            "status": "processed",
            "layer": ProcessingLayer.EDGE,
            "node_id": self.node_id,
            "alert": alert,
            "data": data
        }
    
    def sync_to_cloud(self) -> List[SensorData]:
        """Sincroniza buffer com a nuvem"""
        data_to_sync = self.data_buffer.copy()
        self.data_buffer.clear()
        return data_to_sync


@dataclass
class CloudServer:
    """Servidor na nuvem"""
    server_id: str
    processing_capacity: float
    storage_capacity: float
    total_data_received: int = 0
    analytics_results: List[Dict] = field(default_factory=list)
    
    def process_batch(self, data_batch: List[SensorData]) -> Dict:
        """Processa lote de dados com analytics avançado"""
        self.total_data_received += len(data_batch)
        
        if not data_batch:
            return {"status": "no_data"}
        
        # Análise agregada
        by_type = {}
        for data in data_batch:
            sensor_type = data.sensor_type.value
            if sensor_type not in by_type:
                by_type[sensor_type] = []
            by_type[sensor_type].append(data.value)
        
        analytics = {
            "timestamp": datetime.now(),
            "total_records": len(data_batch),
            "statistics": {}
        }
        
        for sensor_type, values in by_type.items():
            analytics["statistics"][sensor_type] = {
                "count": len(values),
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
        
        self.analytics_results.append(analytics)
        return analytics


class HybridArchitectureSimulator:
    """Simulador de arquitetura híbrida"""
    
    def __init__(self):
        self.edge_nodes: List[EdgeNode] = []
        self.cloud_server: CloudServer = None
        self.sensors: Dict[str, SensorType] = {}
        self.simulation_time: int = 0
        self.metrics = {
            "total_data_generated": 0,
            "edge_processed": 0,
            "cloud_processed": 0,
            "alerts_generated": 0,
            "edge_failures": 0
        }
    
    def setup_infrastructure(self):
        """Configura a infraestrutura de edge e cloud"""
        print("=" * 70)
        print("CONFIGURANDO INFRAESTRUTURA")
        print("=" * 70)
        
        # Criar servidor na nuvem
        self.cloud_server = CloudServer(
            server_id="CLOUD-01",
            processing_capacity=10000.0,
            storage_capacity=100000.0
        )
        print(f"✓ Servidor Cloud criado: {self.cloud_server.server_id}")
        
        # Criar nós de edge
        edge_locations = [
            (-23.5505, -46.6333),  # São Paulo
            (-22.9068, -43.1729),  # Rio de Janeiro
            (-15.7801, -47.9292),  # Brasília
        ]
        
        for i, location in enumerate(edge_locations, 1):
            node = EdgeNode(
                node_id=f"EDGE-{i:02d}",
                location=location,
                processing_capacity=1000.0,
                storage_capacity=5000.0
            )
            self.edge_nodes.append(node)
            print(f"✓ Nó Edge criado: {node.node_id} @ {location}")
        
        # Criar sensores
        sensor_types = list(SensorType)
        for i in range(15):
            sensor_id = f"SENSOR-{i+1:03d}"
            sensor_type = sensor_types[i % len(sensor_types)]
            self.sensors[sensor_id] = sensor_type
            
            # Distribuir sensores entre nós edge
            edge_node = self.edge_nodes[i % len(self.edge_nodes)]
            edge_node.connected_sensors.append(sensor_id)
        
        print(f"✓ {len(self.sensors)} sensores criados e distribuídos")
        print()
    
    def generate_sensor_reading(self, sensor_id: str) -> SensorData:
        """Gera leitura simulada de sensor"""
        sensor_type = self.sensors[sensor_id]
        
        # Valores simulados baseados no tipo de sensor
        min_val, max_val = SENSOR_VALUE_RANGES[sensor_type.name]
        value = random.uniform(min_val, max_val)
        
        # Localização aleatória na região
        location = (
            random.uniform(-25.0, -15.0),
            random.uniform(-50.0, -40.0)
        )
        
        return SensorData(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            value=value,
            timestamp=datetime.now(),
            location=location
        )
    
    def simulate_edge_failure(self):
        """Simula falha aleatória em nó edge (resiliência)"""
        if random.random() < EDGE_FAILURE_PROBABILITY:
            node = random.choice(self.edge_nodes)
            node.is_online = False
            self.metrics["edge_failures"] += 1
            return node.node_id
        return None
    
    def recover_edge_node(self, node_id: str):
        """Recupera nó edge (resiliência)"""
        for node in self.edge_nodes:
            if node.node_id == node_id:
                node.is_online = True
                return True
        return False
    
    def run_simulation_cycle(self):
        """Executa um ciclo de simulação"""
        print(f"\n{'=' * 70}")
        print(f"CICLO DE SIMULAÇÃO #{self.simulation_time + 1}")
        print(f"{'=' * 70}")
        
        # Gerar dados dos sensores
        sensor_readings = []
        for sensor_id in self.sensors:
            reading = self.generate_sensor_reading(sensor_id)
            sensor_readings.append(reading)
            self.metrics["total_data_generated"] += 1
        
        print(f"📊 {len(sensor_readings)} leituras de sensores geradas")
        
        # Processar no edge
        processed_at_edge = []
        alerts = []
        
        for reading in sensor_readings:
            # Encontrar nó edge responsável
            edge_node = None
            for node in self.edge_nodes:
                if reading.sensor_id in node.connected_sensors:
                    edge_node = node
                    break
            
            if edge_node:
                result = edge_node.process_data(reading)
                if result["status"] == "processed":
                    processed_at_edge.append(result)
                    self.metrics["edge_processed"] += 1
                    if result["alert"]:
                        alerts.append(result)
                        self.metrics["alerts_generated"] += 1
        
        print(f"⚡ Edge processou {len(processed_at_edge)} registros")
        if alerts:
            print(f"⚠️  {len(alerts)} alertas gerados no Edge:")
            for alert in alerts[:3]:  # Mostrar apenas 3 primeiros
                print(f"   - {alert['data']}")
        
        # Simular resiliência (falhas e recuperação)
        failed_node = self.simulate_edge_failure()
        if failed_node:
            print(f"❌ Nó {failed_node} falhou! (teste de resiliência)")
            # Recuperar imediatamente
            self.recover_edge_node(failed_node)
            print(f"✓ Nó {failed_node} recuperado (sistema resiliente)")
        
        # Sincronizar com cloud
        all_data_for_cloud = []
        for node in self.edge_nodes:
            data = node.sync_to_cloud()
            all_data_for_cloud.extend(data)
        
        if all_data_for_cloud:
            cloud_result = self.cloud_server.process_batch(all_data_for_cloud)
            self.metrics["cloud_processed"] += cloud_result.get("total_records", 0)
            
            print(f"☁️  Cloud processou {cloud_result.get('total_records', 0)} registros")
            if "statistics" in cloud_result:
                print(f"   Análise agregada de {len(cloud_result['statistics'])} tipos de sensores")
        
        self.simulation_time += 1
    
    def print_summary(self):
        """Imprime sumário da simulação"""
        print(f"\n{'=' * 70}")
        print("SUMÁRIO DA SIMULAÇÃO")
        print(f"{'=' * 70}")
        print(f"Tempo de simulação: {self.simulation_time} ciclos")
        print(f"\nInfraestrutura:")
        print(f"  - Servidor Cloud: 1")
        print(f"  - Nós Edge: {len(self.edge_nodes)}")
        print(f"  - Sensores: {len(self.sensors)}")
        
        print(f"\nMétricas:")
        print(f"  - Dados gerados: {self.metrics['total_data_generated']}")
        print(f"  - Processados no Edge: {self.metrics['edge_processed']}")
        print(f"  - Processados na Cloud: {self.metrics['cloud_processed']}")
        print(f"  - Alertas gerados: {self.metrics['alerts_generated']}")
        print(f"  - Falhas de Edge (recuperadas): {self.metrics['edge_failures']}")
        
        print(f"\nDesempenho dos Nós Edge:")
        for node in self.edge_nodes:
            status = "🟢 Online" if node.is_online else "🔴 Offline"
            print(f"  - {node.node_id}: {node.processed_data} registros processados | {status}")
        
        print(f"\nCloud Analytics:")
        print(f"  - Total de dados recebidos: {self.cloud_server.total_data_received}")
        print(f"  - Análises realizadas: {len(self.cloud_server.analytics_results)}")
        
        if self.cloud_server.analytics_results:
            last_analytics = self.cloud_server.analytics_results[-1]
            print(f"\n  Última análise agregada:")
            for sensor_type, stats in last_analytics["statistics"].items():
                print(f"    {sensor_type}:")
                print(f"      Média: {stats['mean']:.2f}")
                print(f"      Min/Max: {stats['min']:.2f} / {stats['max']:.2f}")
        
        print(f"\n{'=' * 70}")
        print("✓ SIMULAÇÃO CONCLUÍDA COM SUCESSO")
        print(f"{'=' * 70}\n")
    
    def run(self, cycles: int = 3):
        """Executa a simulação completa"""
        print("\n" + "=" * 70)
        print("SIMULADOR DE ARQUITETURA HÍBRIDA COM EDGE COMPUTING")
        print("Para Agro Remoto")
        print("=" * 70 + "\n")
        
        # Setup
        self.setup_infrastructure()
        
        # Executar ciclos de simulação
        for _ in range(cycles):
            self.run_simulation_cycle()
            time.sleep(0.5)  # Pausa para visualização
        
        # Sumário final
        self.print_summary()


def main():
    """Função principal"""
    simulator = HybridArchitectureSimulator()
    simulator.run(cycles=3)


if __name__ == "__main__":
    main()
