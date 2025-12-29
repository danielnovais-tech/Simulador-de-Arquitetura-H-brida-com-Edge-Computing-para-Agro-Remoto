#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Autor: Sistema de Análise de Infraestrutura
Descrição: Simula rede híbrida, edge computing resiliente e testes de validação
"""

import time
import random
import threading
import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

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
    def __init__(self, farm_name: str):
        self.farm_name = farm_name
        self.network_links = self._initialize_links()
        self.edge_nodes = self._initialize_nodes()
        self.telemetry_queue = []
        self.kpis = {
            'availability': 100.0,
            'avg_latency': 0.0,
            'failover_count': 0,
            'messages_delivered': 0,
            'messages_lost': 0,
            'productivity_gain': 0.0
        }
        self.running = False
        self.sd_wan_policy = "starlink_primary"
        
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
        return {
            'edge-01': EdgeNode(
                node_id="edge-01",
                role=NodeRole.ACTIVE,
                k3s_status=True,
                mqtt_connected=True,
                cpu_usage=35.0,
                mem_usage=42.0,
                last_heartbeat=now
            ),
            'edge-02': EdgeNode(
                node_id="edge-02",
                role=NodeRole.ACTIVE,
                k3s_status=True,
                mqtt_connected=True,
                cpu_usage=28.0,
                mem_usage=38.0,
                last_heartbeat=now
            )
        }
    
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
            else:
                node.k3s_status = True
                node.mqtt_connected = True
    
    def _activate_failover(self, failed_node_id: str):
        """Ativa failover para nó standby"""
        standby_nodes = [n for n in self.edge_nodes.values() 
                        if n.node_id != failed_node_id and n.k3s_status]
        
        if standby_nodes:
            standby_nodes[0].role = NodeRole.ACTIVE
            print(f"[Edge] 🔄 Failover ativado para {standby_nodes[0].node_id}")
    
    def generate_telemetry(self):
        """Gera dados de telemetria simulados"""
        sensors = [
            ("temp-001", "temperature", 22.5, "field-north"),
            ("humid-001", "humidity", 65.0, "field-north"),
            ("soil-001", "moisture", 42.0, "field-south"),
            ("camera-001", "image", 1.0, "entrance"),  # valor representa confiança
            ("harvester-001", "actuator", 0.75, "field-central")  # 75% de produtividade
        ]
        
        for sensor_id, data_type, base_value, location in sensors:
            # Adiciona ruído aos dados
            noise = random.uniform(-2.0, 2.0)
            value = max(0.0, base_value + noise)
            
            # Cria hash para integridade
            data_str = f"{sensor_id}{value}{datetime.now().timestamp()}"
            data_hash = hashlib.sha256(data_str.encode()).hexdigest()[:16]
            
            telemetry = TelemetryData(
                sensor_id=sensor_id,
                data_type=data_type,
                value=value,
                timestamp=datetime.now(),
                location=location,
                data_hash=data_hash
            )
            
            self.telemetry_queue.append(telemetry)
            self.kpis['messages_delivered'] += 1
            
            # Simula perda ocasional (1% de chance)
            if random.random() < 0.01:
                self.kpis['messages_lost'] += 1
                print(f"[Telemetry] 📉 Mensagem perdida do sensor {sensor_id}")
    
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
            # Desliga nó edge
            self.edge_nodes['edge-01'].k3s_status = False
            self.edge_nodes['edge-01'].mqtt_connected = False
            print("🖥️  Nó edge-01 desligado forçadamente")
            
        elif test_type == "traffic_spike":
            # Simula pico de tráfego
            for _ in range(50):
                self.generate_telemetry()
            print("📈 Pico de tráfego simulado (50 mensagens)")
        
        # Mede tempo de recuperação
        start_time = time.time()
        recovery_time = None
        
        for i in range(10):  # Monitora por 10 ciclos
            time.sleep(1)
            if test_type == "link_failure":
                if self.sd_wan_policy == "4g_failover":
                    recovery_time = time.time() - start_time
                    break
            elif test_type == "node_failure":
                if self.edge_nodes['edge-02'].role == NodeRole.ACTIVE:
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
        
        telemetry_thread = threading.Thread(target=telemetry_worker, daemon=True)
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
                self.__init__(self.farm_name)
            
            time.sleep(3)
        
        self.running = False
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

def main():
    """Função principal de execução"""
    print("="*60)
    print("ARQUITETURA HÍBRIDA EDGE COMPUTING - AGRO REMOTO")
    print("="*60)
    
    # Inicializa simuladores
    farm_simulator = AgroEdgeSimulator("Fazenda Modelo SP-01")
    nse3000 = NSE3000Simulator()
    
    # Configura NSE3000
    print("\n🔧 Configurando NSE3000...")
    nse3000.configure_vlan('ot_network', 'sensor-temp-001')
    nse3000.configure_vlan('ot_network', 'actuator-harvester-001')
    nse3000.configure_vlan('it_network', 'edge-01')
    nse3000.configure_vlan('it_network', 'edge-02')
    nse3000.create_ipsec_tunnel("cloud-agro-brasil.azure.com")
    nse3000.apply_zero_trust_policy("edge-01", "spiffe://agro/edge/node-01")
    
    # Executa simulação principal
    print("\n🚀 Iniciando simulação da arquitetura...")
    farm_simulator.run_simulation(duration=120)  # 2 minutos para demonstração
    
    # Exporta configuração
    print("\n💾 Exportando configuração para deploy...")
    config = {
        'architecture': 'hybrid_edge_agro',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'network_links': [asdict(link) for link in farm_simulator.network_links.values()],
            'edge_nodes': [asdict(node) for node in farm_simulator.edge_nodes.values()],
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
