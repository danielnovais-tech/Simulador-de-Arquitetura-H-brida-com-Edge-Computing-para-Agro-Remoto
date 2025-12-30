#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Este simulador demonstra uma arquitetura híbrida de edge computing para agricultura remota,
incluindo sensores IoT, dispositivos edge, e processamento em nuvem.
"""

import argparse
import time
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class SensorData:
    """Dados coletados de sensores agrícolas"""
    sensor_id: str
    timestamp: float
    temperature: float
    humidity: float
    soil_moisture: float
    light_level: float
    location: str


@dataclass_json
@dataclass
class EdgeDevice:
    """Dispositivo Edge para processamento local"""
    device_id: str
    location: str
    processing_capacity: float
    battery_level: float = 100.0
    is_online: bool = True
    processed_count: int = 0
    
    def process_data(self, sensor_data: SensorData) -> Dict:
        """Processa dados localmente no edge"""
        self.processed_count += 1
        self.battery_level = max(0, self.battery_level - 0.1)
        
        # Análise local de dados
        analysis = {
            "device_id": self.device_id,
            "sensor_id": sensor_data.sensor_id,
            "timestamp": sensor_data.timestamp,
            "location": sensor_data.location,
            "irrigation_needed": sensor_data.soil_moisture < 30.0,
            "temperature_alert": sensor_data.temperature > 35.0 or sensor_data.temperature < 5.0,
            "humidity_alert": sensor_data.humidity < 20.0 or sensor_data.humidity > 90.0,
            "processed_at_edge": True,
            "battery_level": self.battery_level
        }
        
        return analysis


@dataclass_json
@dataclass
class CloudServer:
    """Servidor em nuvem para processamento avançado"""
    server_id: str
    total_data_received: int = 0
    storage_used_mb: float = 0.0
    alerts_generated: int = 0
    
    def process_edge_data(self, edge_analysis: Dict) -> Dict:
        """Processa dados recebidos dos dispositivos edge"""
        self.total_data_received += 1
        self.storage_used_mb += 0.05
        
        # Análise avançada em nuvem
        advanced_analysis = {
            **edge_analysis,
            "cloud_processed": True,
            "ml_prediction": self._generate_prediction(edge_analysis),
            "recommendations": self._generate_recommendations(edge_analysis)
        }
        
        if edge_analysis.get("irrigation_needed") or edge_analysis.get("temperature_alert"):
            self.alerts_generated += 1
            advanced_analysis["alert_level"] = "high" if edge_analysis.get("temperature_alert") else "medium"
        
        return advanced_analysis
    
    def _generate_prediction(self, data: Dict) -> str:
        """Gera predições usando ML simulado"""
        predictions = [
            "Condições favoráveis para crescimento",
            "Risco de stress hídrico em 24h",
            "Temperatura ideal mantida",
            "Umidade adequada para a cultura"
        ]
        return random.choice(predictions)
    
    def _generate_recommendations(self, data: Dict) -> List[str]:
        """Gera recomendações baseadas nos dados"""
        recommendations = []
        
        if data.get("irrigation_needed"):
            recommendations.append("Ativar sistema de irrigação")
        
        if data.get("temperature_alert"):
            recommendations.append("Verificar sistema de ventilação/aquecimento")
        
        if data.get("humidity_alert"):
            recommendations.append("Ajustar umidade do ambiente")
        
        if not recommendations:
            recommendations.append("Manter monitoramento contínuo")
        
        return recommendations


@dataclass
class HybridEdgeSimulator:
    """Simulador principal da arquitetura híbrida"""
    num_sensors: int = 5
    num_edge_devices: int = 2
    duration: int = 60
    edge_devices: List[EdgeDevice] = field(default_factory=list)
    cloud: Optional[CloudServer] = None
    total_data_points: int = 0
    start_time: float = 0.0
    
    def __post_init__(self):
        """Inicializa dispositivos edge e servidor em nuvem"""
        locations = ["Campo A", "Campo B", "Estufa 1", "Estufa 2", "Área de Cultivo C"]
        
        # Criar dispositivos edge
        for i in range(self.num_edge_devices):
            self.edge_devices.append(EdgeDevice(
                device_id=f"edge_{i+1}",
                location=locations[i % len(locations)],
                processing_capacity=random.uniform(0.8, 1.0)
            ))
        
        # Criar servidor em nuvem
        self.cloud = CloudServer(server_id="cloud_main")
    
    def generate_sensor_data(self, sensor_id: int) -> SensorData:
        """Gera dados simulados de sensores"""
        locations = ["Campo A", "Campo B", "Estufa 1", "Estufa 2", "Área de Cultivo C"]
        
        return SensorData(
            sensor_id=f"sensor_{sensor_id}",
            timestamp=time.time(),
            temperature=random.uniform(15.0, 40.0),
            humidity=random.uniform(10.0, 95.0),
            soil_moisture=random.uniform(10.0, 80.0),
            light_level=random.uniform(0.0, 100.0),
            location=locations[sensor_id % len(locations)]
        )
    
    def run_simulation(self):
        """Executa a simulação"""
        print("=" * 80)
        print("SIMULADOR DE ARQUITETURA HÍBRIDA COM EDGE COMPUTING PARA AGRO REMOTO")
        print("=" * 80)
        print(f"\nConfiguração:")
        print(f"  - Sensores: {self.num_sensors}")
        print(f"  - Dispositivos Edge: {self.num_edge_devices}")
        print(f"  - Duração: {self.duration} segundos")
        print(f"  - Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "=" * 80)
        
        self.start_time = time.time()
        iteration = 0
        
        while (time.time() - self.start_time) < self.duration:
            iteration += 1
            print(f"\n[Iteração {iteration}] Tempo: {int(time.time() - self.start_time)}s / {self.duration}s")
            
            # Coletar dados de sensores
            for sensor_id in range(self.num_sensors):
                sensor_data = self.generate_sensor_data(sensor_id)
                self.total_data_points += 1
                
                # Selecionar dispositivo edge para processar
                edge_device = self.edge_devices[sensor_id % len(self.edge_devices)]
                
                # Processar no edge
                edge_analysis = edge_device.process_data(sensor_data)
                
                # Enviar para nuvem
                cloud_analysis = self.cloud.process_edge_data(edge_analysis)
                
                # Exibir resultados interessantes
                if cloud_analysis.get("alert_level") or iteration == 1:
                    print(f"  └─ {sensor_data.sensor_id} ({sensor_data.location}):")
                    print(f"     Temp: {sensor_data.temperature:.1f}°C | "
                          f"Umidade: {sensor_data.humidity:.1f}% | "
                          f"Solo: {sensor_data.soil_moisture:.1f}%")
                    
                    if cloud_analysis.get("recommendations"):
                        print(f"     Recomendações: {', '.join(cloud_analysis['recommendations'])}")
            
            # Status dos dispositivos edge
            if iteration % 3 == 0:
                print("\n  Dispositivos Edge:")
                for device in self.edge_devices:
                    print(f"    - {device.device_id} ({device.location}): "
                          f"Bateria {device.battery_level:.1f}%, "
                          f"{device.processed_count} dados processados")
            
            # Pausa entre iterações
            time.sleep(2)
        
        # Relatório final
        self.print_final_report(time.time() - self.start_time)
    
    def print_final_report(self, elapsed_time: float):
        """Imprime relatório final da simulação"""
        print("\n" + "=" * 80)
        print("RELATÓRIO FINAL DA SIMULAÇÃO")
        print("=" * 80)
        print(f"\nDuração Real: {elapsed_time:.2f} segundos")
        print(f"Total de Pontos de Dados: {self.total_data_points}")
        print(f"\nEstatísticas da Nuvem:")
        print(f"  - Dados recebidos: {self.cloud.total_data_received}")
        print(f"  - Armazenamento usado: {self.cloud.storage_used_mb:.2f} MB")
        print(f"  - Alertas gerados: {self.cloud.alerts_generated}")
        
        print(f"\nEstatísticas dos Dispositivos Edge:")
        for device in self.edge_devices:
            print(f"  - {device.device_id} ({device.location}):")
            print(f"    * Dados processados: {device.processed_count}")
            print(f"    * Bateria restante: {device.battery_level:.1f}%")
            print(f"    * Status: {'Online' if device.is_online else 'Offline'}")
        
        if elapsed_time > 0:
            processing_rate = self.total_data_points / elapsed_time
        else:
            processing_rate = 0.0

        if self.total_data_points > 0:
            edge_efficiency = (
                sum(d.processed_count for d in self.edge_devices) / self.total_data_points * 100
            )
        else:
            edge_efficiency = 0.0

        print(f"\nTaxa de Processamento: {processing_rate:.2f} dados/segundo")
        print(f"Eficiência Edge: {edge_efficiency:.1f}%")
        print("\n" + "=" * 80)
        print("Simulação concluída com sucesso!")
        print("=" * 80)


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python agro_edge_simulator.py                    # Executa com duração padrão (60s)
  python agro_edge_simulator.py --duration 600     # Executa por 10 minutos
  python agro_edge_simulator.py --duration 120     # Executa por 2 minutos
        """
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Duração da simulação em segundos (padrão: 60)'
    )
    
    parser.add_argument(
        '--sensors',
        type=int,
        default=5,
        help='Número de sensores a simular (padrão: 5)'
    )
    
    parser.add_argument(
        '--edge-devices',
        type=int,
        default=2,
        help='Número de dispositivos edge (padrão: 2)'
    )
    
    args = parser.parse_args()
    
    # Validações
    if args.duration < 1:
        print("Erro: A duração deve ser pelo menos 1 segundo")
        return 1
    
    if args.sensors < 1:
        print("Erro: Deve haver pelo menos 1 sensor")
        return 1
    
    if args.edge_devices < 1:
        print("Erro: Deve haver pelo menos 1 dispositivo edge")
        return 1
    
    # Criar e executar simulador
    simulator = HybridEdgeSimulator(
        num_sensors=args.sensors,
        num_edge_devices=args.edge_devices,
        duration=args.duration
    )
    
    try:
        simulator.run_simulation()
        return 0
    except KeyboardInterrupt:
        print("\n\nSimulação interrompida pelo usuário.")
        simulator.print_final_report(time.time() - simulator.start_time)
        return 0
    except Exception as e:
        print(f"\nErro durante a simulação: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
