#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Hybrid Architecture Simulator with Edge Computing for Remote Agriculture

Author: Infrastructure Analysis System
Description: Simulates hybrid network, resilient edge computing and validation tests

Usage:
    python3 simulador_agro_edge.py [--duration <seconds>] [--sensors <n>] [--edges <n>] [--cloud-prob <0..1>]
    
    Example:
        python3 simulador_agro_edge.py --duration 300
        
    Arguments:
        --duration: Simulation duration in seconds (positive integer, default: 300)
        --sensors: Number of simulated IoT sensors (positive integer, default: 9)
        --edges: Number of edge nodes (positive integer, default: 3)
        --cloud-prob: Probability (0.0-1.0) that telemetry is sent to cloud instead of edge queue (default: 0.3)
        --version: Show version and exit
"""

import time
import random
import threading
import json
import argparse
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import hashlib

# ============ ANSI COLOR CONSTANTS ============
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# ============ ENUMS E ESTRUTURAS ============

class LinkStatus(Enum):
    ONLINE = "online"
    DEGRADED = "degraded"
    OFFLINE = "offline"

class NodeRole(Enum):
    ACTIVE = "active"
    STANDBY = "standby"

@dataclass
class NetworkLink:
    name: str
    link_type: str  # "starlink", "4g", "lte", "lora"
    status: LinkStatus
    latency: float  # ms
    bandwidth: float  # Mbps
    last_failover: Optional[datetime] = None

@dataclass
class EdgeNode:
    node_id: str
    role: NodeRole
    k3s_status: bool
    mqtt_connected: bool
    cpu_usage: float
    mem_usage: float
    last_heartbeat: datetime

@dataclass
class TelemetryData:
    sensor_id: str
    data_type: str  # "temperature", "humidity", "image", "actuator"
    value: float
    timestamp: datetime
    location: str
    data_hash: str

# ============ CLASSE PRINCIPAL DE SIMULAÇÃO ============

class AgroEdgeSimulator:
    """
    Main simulator for hybrid architecture with edge computing.
    
    Thread Safety:
        - telemetry_queue: Access is serialized via GIL (Python list operations are atomic)
        - kpis: Dictionary access is protected by GIL for atomic updates
        - For production use, consider using threading.Lock or queue.Queue for explicit safety
    """
    def __init__(self, farm_name: str, *, num_sensors: int = 9, num_edges: int = 3, cloud_prob: float = 0.3):
        self.farm_name = farm_name
        self.num_sensors = num_sensors
        self.num_edges = num_edges
        self.cloud_prob = cloud_prob
        self.network_links = self._initialize_links()
        self.edge_nodes = self._initialize_nodes()
        self.sensors = self._initialize_sensors()
        self.telemetry_queue = []
        self.kpis = {
            'availability': 100.0,
            'avg_latency': 0.0,
            'failover_count': 0,
            'messages_delivered': 0,
            'messages_lost': 0,
            'productivity_gain': 0.0,
            'edge_messages': 0,
            'cloud_messages': 0
        }
        self.running = False
        self.sd_wan_policy = "starlink_primary"
    
    def _reset_after_chaos_test(self):
        """Restaura estado após teste de caos"""
        # Restaura links de rede
        self.network_links['starlink'].status = LinkStatus.ONLINE
        self.network_links['starlink'].latency = 45.0
        self.sd_wan_policy = "starlink_primary"
        
        # Restaura nós edge
        for node in self.edge_nodes.values():
            node.k3s_status = True
            node.mqtt_connected = True
        
        # Limpa fila de telemetria excessiva (mantém últimas 10 mensagens)
        if len(self.telemetry_queue) > 10:
            self.telemetry_queue = self.telemetry_queue[-10:]
        
    def _initialize_links(self) -> Dict[str, NetworkLink]:
        """Inicializa os links de rede"""
        return {
            'starlink': NetworkLink(
                name="Starlink-001",
                link_type="starlink",
                status=LinkStatus.ONLINE,
                latency=45.0,
                bandwidth=150.0
            ),
            '4g_backup': NetworkLink(
                name="4G-Rural-01",
                link_type="4g",
                status=LinkStatus.ONLINE,
                latency=85.0,
                bandwidth=30.0
            ),
            'lora_mesh': NetworkLink(
                name="LoRa-Mesh-01",
                link_type="lora",
                status=LinkStatus.ONLINE,
                latency=120.0,
                bandwidth=0.05
            )
        }
    
    def _initialize_nodes(self) -> Dict[str, EdgeNode]:
        """Inicializa nós edge em configuração active-active"""
        now = datetime.now()
        nodes: Dict[str, EdgeNode] = {}

        # Keep an active-active flavor: first two nodes start ACTIVE (if present),
        # remaining nodes start STANDBY and may be promoted during failover.
        for i in range(self.num_edges):
            node_id = f"edge-{i+1:02d}"
            role = NodeRole.ACTIVE if i < 2 else NodeRole.STANDBY
            nodes[node_id] = EdgeNode(
                node_id=node_id,
                role=role,
                k3s_status=True,
                mqtt_connected=True,
                cpu_usage=random.uniform(20.0, 45.0),
                mem_usage=random.uniform(30.0, 55.0),
                last_heartbeat=now
            )

        return nodes

    def _initialize_sensors(self) -> List[Tuple[str, str, float, str]]:
        """Inicializa uma lista de sensores simulados (id, tipo, valor_base, localização)."""
        base_sensors: List[Tuple[str, str, float, str]] = [
            ("temp-001", "temperature", 22.5, "field-north"),
            ("humid-001", "humidity", 65.0, "field-north"),
            ("soil-001", "moisture", 42.0, "field-south"),
            ("camera-001", "image", 1.0, "entrance"),
            ("harvester-001", "actuator", 0.75, "field-central"),
        ]

        if self.num_sensors <= len(base_sensors):
            return base_sensors[: self.num_sensors]

        sensors: List[Tuple[str, str, float, str]] = list(base_sensors)
        extra = self.num_sensors - len(base_sensors)

        extra_types: List[Tuple[str, str, float, str]] = [
            ("temp", "temperature", 23.0, "field-west"),
            ("humid", "humidity", 62.0, "field-east"),
            ("soil", "moisture", 40.0, "field-central"),
        ]

        for i in range(extra):
            prefix, data_type, base_value, location = extra_types[i % len(extra_types)]
            sensors.append((f"{prefix}-{i+2:03d}", data_type, base_value, location))

        return sensors
    
    def simulate_sd_wan_orchestration(self):
        """Simula orquestração SD-WAN para failover"""
        primary = self.network_links['starlink']
        
        # Simula falha no link primário (10% de chance)
        if random.random() < 0.1:
            primary.status = LinkStatus.OFFLINE
            primary.latency = 999.0
            print(f"[SD-WAN] ⚠️  Falha detectada no link primário: {primary.name}")
            
            # Executa failover para 4G
            if self.network_links['4g_backup'].status == LinkStatus.ONLINE:
                self.sd_wan_policy = "4g_failover"
                primary.last_failover = datetime.now()
                self.kpis['failover_count'] += 1
                print(f"[SD-WAN] ✅ Failover para 4G em {datetime.now()}")
        
        # Recuperação do link primário
        elif primary.status == LinkStatus.OFFLINE and random.random() < 0.3:
            primary.status = LinkStatus.ONLINE
            primary.latency = 45.0
            self.sd_wan_policy = "starlink_primary"
            print(f"[SD-WAN] 🔄 Link primário recuperado")
    
    def simulate_edge_heartbeat(self):
        """Simula heartbeat entre nós edge"""
        now = datetime.now()
        
        for node_id, node in self.edge_nodes.items():
            # Simula pequenas variações
            node.cpu_usage = max(5.0, min(80.0, node.cpu_usage + random.uniform(-5, 5)))
            node.mem_usage = max(30.0, min(90.0, node.mem_usage + random.uniform(-2, 2)))
            node.last_heartbeat = now
            
            # Simula falha de nó (2% de chance)
            if random.random() < 0.02:
                node.k3s_status = False
                node.mqtt_connected = False
                print(f"[Edge] ❌ Nó {node_id} falhou")
                
                # Ativa failover automático
                if node.role == NodeRole.ACTIVE:
                    self._activate_failover(node_id)
            elif not node.k3s_status or not node.mqtt_connected:
                # Restaura nós previamente falhados
                node.k3s_status = True
                node.mqtt_connected = True
    
    def _activate_failover(self, failed_node_id: str):
        """Ativa failover para nó standby"""
        candidates = [
            n for n in self.edge_nodes.values()
            if n.node_id != failed_node_id and n.k3s_status and n.mqtt_connected
        ]

        # Prefer promoting STANDBY nodes first.
        standby_candidates = [n for n in candidates if n.role == NodeRole.STANDBY]
        target = (standby_candidates[0] if standby_candidates else (candidates[0] if candidates else None))

        if target:
            target.role = NodeRole.ACTIVE
            print(f"[Edge] 🔄 Failover ativado para {target.node_id}")
    
    def generate_telemetry(self):
        """Gera dados de telemetria simulados"""
        for sensor_id, data_type, base_value, location in self.sensors:
            # Adiciona ruído aos dados
            noise = random.uniform(-2.0, 2.0)
            value = max(0.0, base_value + noise)
            
            # Cria hash para integridade
            data_str = f"{sensor_id}{value}{datetime.now().timestamp()}"
            data_hash = hashlib.sha256(data_str.encode()).hexdigest()
            
            telemetry = TelemetryData(
                sensor_id=sensor_id,
                data_type=data_type,
                value=value,
                timestamp=datetime.now(),
                location=location,
                data_hash=data_hash
            )
            
            # Simula perda ocasional (1% de chance)
            if random.random() < 0.01:
                self.kpis['messages_lost'] += 1
                print(f"[Telemetry] 📉 Mensagem perdida do sensor {sensor_id}")
            else:
                self.kpis['messages_delivered'] += 1

                # Decide se telemetria vai para cloud ou para a fila local (edge)
                if random.random() < self.cloud_prob:
                    self.kpis['cloud_messages'] += 1
                else:
                    self.telemetry_queue.append(telemetry)
                    self.kpis['edge_messages'] += 1
    
    def process_edge_inference(self):
        """Simula inferência local com visão computacional"""
        if not self.telemetry_queue:
            return
        
        # Processa até 5 mensagens por ciclo
        for _ in range(min(5, len(self.telemetry_queue))):
            if self.telemetry_queue:
                data = self.telemetry_queue.pop(0)
                
                # Simula processamento de imagem para colheita autônoma
                if data.data_type == "image":
                    if data.value > 0.8:  # Alta confiança
                        print(f"[Inference] ✅ Planta identificada para colheita (conf: {data.value:.2f})")
                        self.kpis['productivity_gain'] = min(
                            35.0,  # Máximo de 35%
                            self.kpis['productivity_gain'] + 0.1
                        )
    
    def update_kpis(self):
        """Atualiza KPIs em tempo real"""
        # Calcula disponibilidade baseada em status dos links
        online_links = sum(1 for link in self.network_links.values() 
                          if link.status == LinkStatus.ONLINE)
        total_links = len(self.network_links)
        self.kpis['availability'] = (online_links / total_links) * 100
        
        # Latência média ponderada
        latencies = [link.latency for link in self.network_links.values()]
        self.kpis['avg_latency'] = sum(latencies) / len(latencies)
        
        # Simula ganho de produtividade incremental
        if random.random() < 0.2:  # 20% de chance de incremento por ciclo
            self.kpis['productivity_gain'] = min(
                35.0,
                self.kpis['productivity_gain'] + random.uniform(0.05, 0.2)
            )
    
    def run_chaos_test(self, test_type: str):
        """Executa testes de caos controlados"""
        print(f"\n[Chaos Test] Iniciando teste: {test_type}")
        
        if test_type == "link_failure":
            # Desliga link primário
            self.network_links['starlink'].status = LinkStatus.OFFLINE
            print("🔗 Link Starlink desligado forçadamente")
            
        elif test_type == "node_failure":
            # Desliga nó edge (primeiro nó disponível)
            if len(self.edge_nodes) < 2:
                print("🖥️  Teste ignorado: é necessário ao menos 2 edge nodes para validar failover")
                return True

            failed_id = sorted(self.edge_nodes.keys())[0]
            self.edge_nodes[failed_id].k3s_status = False
            self.edge_nodes[failed_id].mqtt_connected = False
            self.edge_nodes[failed_id].role = NodeRole.STANDBY
            print(f"🖥️  Nó {failed_id} desligado forçadamente")
            
        elif test_type == "traffic_spike":
            # Simula pico de tráfego
            for _ in range(50):
                self.generate_telemetry()
            print("📈 Pico de tráfego simulado (50 mensagens)")
            print("[Chaos Test] ✅ Teste de pico de tráfego concluído (sem recuperação necessária)")
            return True
        
        # Mede tempo de recuperação para testes que necessitam
        start_time = time.time()
        recovery_time = None
        
        for _ in range(10):  # Monitora por 10 ciclos
            time.sleep(1)
            if test_type == "link_failure":
                # Actively monitor recovery by invoking orchestration
                self.simulate_sd_wan_orchestration()
                if self.sd_wan_policy == "4g_failover":
                    recovery_time = time.time() - start_time
                    break
            elif test_type == "node_failure":
                # Actively monitor recovery by invoking heartbeat
                self.simulate_edge_heartbeat()
                active_healthy = [
                    n for n in self.edge_nodes.values()
                    if n.role == NodeRole.ACTIVE and n.k3s_status and n.mqtt_connected
                ]
                if active_healthy:
                    recovery_time = time.time() - start_time
                    break
        
        if recovery_time:
            print(f"[Chaos Test] ✅ Recuperação em {recovery_time:.2f}s (SLA: <5s)")
            return recovery_time <= 5.0
        else:
            print("[Chaos Test] ❌ Falha na recuperação")
            return False
    
    def print_dashboard(self):
        """Exibe dashboard de status"""
        print("\n" + "="*60)
        print(f"🌾 SIMULADOR AGRO REMOTO - {self.farm_name}")
        print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        print("\n📡 CONECTIVIDADE:")
        for link in self.network_links.values():
            status_icon = "✅" if link.status == LinkStatus.ONLINE else "⚠️" if link.status == LinkStatus.DEGRADED else "❌"
            print(f"  {status_icon} {link.name}: {link.status.value} | "
                  f"Latência: {link.latency:.1f}ms | BW: {link.bandwidth:.1f}Mbps")
        
        print(f"\n🔄 Política SD-WAN: {self.sd_wan_policy}")
        
        print("\n🖥️  EDGE COMPUTING:")
        for node in self.edge_nodes.values():
            k3s_icon = "✅" if node.k3s_status else "❌"
            mqtt_icon = "✅" if node.mqtt_connected else "❌"
            print(f"  {k3s_icon}{mqtt_icon} {node.node_id} ({node.role.value}) | "
                  f"CPU: {node.cpu_usage:.1f}% | Mem: {node.mem_usage:.1f}%")
        
        print("\n📊 KPIs:")
        print(f"  📈 Disponibilidade: {self.kpis['availability']:.2f}%")
        print(f"  ⏱️  Latência média: {self.kpis['avg_latency']:.1f}ms")
        print(f"  🔄 Failovers: {self.kpis['failover_count']}")
        print(f"  📨 Mensagens: {self.kpis['messages_delivered']} entregues, "
              f"{self.kpis['messages_lost']} perdidas")
        print(f"  ☁️  Cloud: {self.kpis['cloud_messages']} | 🧠 Edge: {self.kpis['edge_messages']}")
        print(f"  🚀 Ganho Produtividade: +{self.kpis['productivity_gain']:.2f}%")
        
        print(f"\n📦 Fila de telemetria: {len(self.telemetry_queue)} mensagens")
        print("="*60)
    
    def run_simulation(self, duration: int = 300):
        """Executa simulação principal"""
        print(f"Iniciando simulação por {duration} segundos...")
        self.running = True
        start_time = time.time()
        
        # Thread para geração contínua de telemetria
        def telemetry_worker():
            while self.running:
                self.generate_telemetry()
                time.sleep(2)
        
        telemetry_thread = threading.Thread(target=telemetry_worker)
        telemetry_thread.start()
        
        cycle = 0
        while time.time() - start_time < duration:
            cycle += 1
            print(f"\n🔁 Ciclo {cycle}")
            
            # Executa componentes
            self.simulate_sd_wan_orchestration()
            self.simulate_edge_heartbeat()
            self.process_edge_inference()
            self.update_kpis()
            
            # Exibe dashboard a cada 5 ciclos
            if cycle % 5 == 0:
                self.print_dashboard()
            
            # Executa teste de caos a cada 10 ciclos
            if cycle % 10 == 0:
                tests = ["link_failure", "node_failure", "traffic_spike"]
                test = random.choice(tests)
                self.run_chaos_test(test)
                # Restaura estado após teste
                self._reset_after_chaos_test()
            
            time.sleep(3)
        
        self.running = False
        
        # Aguarda thread de telemetria finalizar
        if telemetry_thread and telemetry_thread.is_alive():
            telemetry_thread.join(timeout=5)
        
        print("\n" + "="*60)
        print("SIMULAÇÃO CONCLUÍDA - RELATÓRIO FINAL:")
        print("="*60)
        self.print_dashboard()
        
        # Avaliação de metas
        print("\n🎯 AVALIAÇÃO DE METAS:")
        sla_ok = self.kpis['availability'] >= 99.5
        latency_ok = self.kpis['avg_latency'] <= 50.0
        productivity_ok = self.kpis['productivity_gain'] >= 30.0
        
        print(f"  {'✅' if sla_ok else '❌'} SLA >99.5%: {self.kpis['availability']:.2f}%")
        print(f"  {'✅' if latency_ok else '❌'} Latência <50ms: {self.kpis['avg_latency']:.1f}ms")
        print(f"  {'✅' if productivity_ok else '❌'} Produtividade +30%: +{self.kpis['productivity_gain']:.2f}%")
        
        if all([sla_ok, latency_ok, productivity_ok]):
            print("\n🎉 TODAS AS METAS ATINGIDAS! Arquitetura validada.")
        else:
            print("\n⚠️  ALGUMAS METAS NÃO ATINGIDAS. Ajustes necessários.")

# ============ NSE3000 SIMULATION ============

class NSE3000Simulator:
    """Simula funcionalidades do switch/segurança NSE3000"""
    
    def __init__(self):
        self.vlan_config = {
            'ot_network': {'id': 10, 'devices': [], 'qos': 'high'},
            'it_network': {'id': 20, 'devices': [], 'qos': 'medium'},
            'management': {'id': 30, 'devices': [], 'qos': 'low'}
        }
        self.ipsec_tunnels = []
        self.security_policies = []
        
    def configure_vlan(self, vlan_name: str, device_id: str):
        """Configura VLAN para segmentação OT/IT"""
        if vlan_name in self.vlan_config:
            self.vlan_config[vlan_name]['devices'].append(device_id)
            print(f"[NSE3000] 🔀 Dispositivo {device_id} movido para VLAN {vlan_name}")
            return True
        return False
    
    def create_ipsec_tunnel(self, remote_endpoint: str):
        """Cria túnel IPsec para backhaul"""
        tunnel = {
            'id': f"tunnel-{len(self.ipsec_tunnels)+1}",
            'remote': remote_endpoint,
            'status': 'active',
            'encryption': 'AES-256-GCM'
        }
        self.ipsec_tunnels.append(tunnel)
        print(f"[NSE3000] 🔐 Túnel IPsec criado para {remote_endpoint}")
        return tunnel
    
    def apply_zero_trust_policy(self, device_id: str, workload_identity: str):
        """Aplica política zero trust"""
        policy = {
            'device': device_id,
            'identity': workload_identity,
            'access': 'minimal_privilege',
            'timestamp': datetime.now()
        }
        self.security_policies.append(policy)
        print(f"[NSE3000] 🛡️  Política zero trust aplicada para {device_id}")
        return policy

# ============ FUNÇÃO PRINCIPAL ============

def positive_int(value):
    """
    Validates that a value is a positive integer.
    
    Args:
        value: String representation of an integer
        
    Returns:
        int: The validated positive integer
        
    Raises:
        argparse.ArgumentTypeError: If value is not a positive integer
    """
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} must be a positive integer")

    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be a positive integer")

    return ivalue


def probability(value):
    """Validates that a value is a float in [0.0, 1.0]."""
    try:
        fvalue = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} não é um número válido")

    if not (0.0 <= fvalue <= 1.0):
        raise argparse.ArgumentTypeError(f"{value} deve estar entre 0.0 e 1.0")

    return fvalue


def serialize_dataclass_with_enums(obj):
    """
    Serializes a dataclass to dict with enum values properly converted.
    
    Args:
        obj: A dataclass instance
        
    Returns:
        dict: Dictionary with enums serialized by their value attribute
    """
    result = asdict(obj)
    # Convert enum fields to their values
    for key, value in result.items():
        if isinstance(value, Enum):
            result[key] = value.value
    return result


def main():
    """Função principal de execução"""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Hybrid Architecture Simulator with Edge Computing for Remote Agriculture',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 simulador_agro_edge.py
  python3 simulador_agro_edge.py --duration 300
  python3 simulador_agro_edge.py --duration 60 --sensors 15 --edges 5 --cloud-prob 0.5
        """
    )
    parser.add_argument(
        '--duration',
        type=positive_int,
        default=300,
        help='Simulation duration in seconds (positive integer, default: 300)'
    )
    parser.add_argument(
        '--sensors',
        type=positive_int,
        default=9,
        help='Number of simulated IoT sensors (positive integer, default: 9)'
    )
    parser.add_argument(
        '--edges',
        type=positive_int,
        default=3,
        help='Number of edge nodes (positive integer, default: 3)'
    )
    parser.add_argument(
        '--cloud-prob',
        type=probability,
        default=0.3,
        help='Probability of sending telemetry to cloud instead of edge queue (0.0-1.0, default: 0.3)'
    )
    parser.add_argument('--version', action='version', version='AgroEdgeSim v1.0')
    
    args = parser.parse_args()
    
    print("="*60)
    print("ARQUITETURA HÍBRIDA EDGE COMPUTING - AGRO REMOTO")
    print("="*60)
    print(f"Duração: {args.duration}s | Sensores: {args.sensors} | Edge nodes: {args.edges} | Cloud prob: {args.cloud_prob:.2f}")
    
    # Inicializa simuladores
    if args.edges < 2:
        print("⚠️  Aviso: --edges < 2 limita testes de failover (node_failure).")

    farm_simulator = AgroEdgeSimulator(
        "Fazenda Modelo SP-01",
        num_sensors=args.sensors,
        num_edges=args.edges,
        cloud_prob=args.cloud_prob,
    )
    nse3000 = NSE3000Simulator()
    
    # Configura NSE3000
    print("\n🔧 Configurando NSE3000...")
    # Map first few simulated sensors into OT network
    for sensor_id, _, _, _ in farm_simulator.sensors[: min(5, len(farm_simulator.sensors))]:
        nse3000.configure_vlan('ot_network', f"sensor-{sensor_id}")

    nse3000.configure_vlan('ot_network', 'actuator-harvester-001')

    # Map all edge nodes into IT network
    for node_id in sorted(farm_simulator.edge_nodes.keys()):
        nse3000.configure_vlan('it_network', node_id)

    nse3000.create_ipsec_tunnel("cloud-agro-brasil.azure.com")
    first_edge = sorted(farm_simulator.edge_nodes.keys())[0] if farm_simulator.edge_nodes else "edge-01"
    nse3000.apply_zero_trust_policy(first_edge, "spiffe://agro/edge/node-01")
    
    # Executa simulação principal
    print("\n🚀 Iniciando simulação da arquitetura...")
    farm_simulator.run_simulation(duration=args.duration)
    
    # Exporta configuração
    print("\n💾 Exportando configuração para deploy...")
    config = {
        'architecture': 'hybrid_edge_agro',
        'timestamp': datetime.now().isoformat(),
        'cli_args': {
            'duration': args.duration,
            'sensors': args.sensors,
            'edges': args.edges,
            'cloud_prob': args.cloud_prob
        },
        'components': {
            'network_links': [serialize_dataclass_with_enums(link) for link in farm_simulator.network_links.values()],
            'edge_nodes': [serialize_dataclass_with_enums(node) for node in farm_simulator.edge_nodes.values()],
            'nse3000_config': {
                'vlans': nse3000.vlan_config,
                'tunnels': nse3000.ipsec_tunnels
            }
        },
        'kpis': farm_simulator.kpis
    }
    
    with open('agro_edge_deploy.json', 'w') as f:
        json.dump(config, f, indent=2, default=str)
    
    print("✅ Configuração exportada para 'agro_edge_deploy.json'")
    print("\n" + "="*60)
    print("PRÓXIMOS PASSOS RECOMENDADOS:")
    print("1. Validar NSE3000 com vendor (L3 switch, firewall, gateway)")
    print("2. Inventário completo de sensores/atuadores")
    print("3. Piloto em 1 fazenda com 2 nós edge")
    print("4. Testes de caos em ambiente controlado")
    print("5. Medição contínua de KPIs (+30% produtividade)")
    print("="*60)

if __name__ == "__main__":
    main()
