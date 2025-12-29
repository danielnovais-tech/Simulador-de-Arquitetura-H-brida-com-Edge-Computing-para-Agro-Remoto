#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Integração NSE3000 com processamento de telemetria e SD-WAN
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import random


@dataclass
class TelemetryData:
    """Dados de telemetria de sensores agrícolas"""
    sensor_id: str
    data_type: str  # temperature, humidity, image, actuator, etc
    value: float
    timestamp: datetime
    location: Optional[str] = None


class NSE3000:
    """Simulador do Fortinet FortiGate NSE3000 para QoS e segurança"""
    
    def __init__(self):
        self.vlans = {
            "ot_network": {"id": 100, "priority": "high"},
            "it_network": {"id": 200, "priority": "medium"},
            "guest_network": {"id": 300, "priority": "low"}
        }
        self.policies_applied = 0
        
    def configure_vlan(self, vlan_name: str, vlan_id: int, priority: str):
        """Configura VLAN no NSE3000"""
        self.vlans[vlan_name] = {"id": vlan_id, "priority": priority}
        print(f"[NSE3000-Config] VLAN '{vlan_name}' configurada: ID={vlan_id}, Priority={priority}")
        
    def get_stats(self):
        """Retorna estatísticas do NSE3000"""
        return {
            "policies_applied": self.policies_applied,
            "vlans_configured": len(self.vlans)
        }


class EdgeComputing:
    """Simulador de Edge Computing com integração NSE3000"""
    
    def __init__(self, nse3000: NSE3000):
        self.nse3000 = nse3000
        self.processed_data = []
        
    def process_edge_inference(self, telemetry: TelemetryData):
        """Processa inferência na borda com aplicação de políticas NSE3000"""
        print(f"\n[Edge-Processing] Recebido dado de {telemetry.sensor_id}")
        
        # Processamento específico por tipo de dado
        if telemetry.data_type == "temperature":
            inference = self._analyze_temperature(telemetry)
        elif telemetry.data_type == "image":
            inference = self._analyze_image(telemetry)
        elif telemetry.data_type == "actuator":
            inference = self._process_actuator_command(telemetry)
        else:
            inference = {"status": "processed", "action": None}
            
        # Aplica políticas NSE3000 integradas ao fluxo
        self.apply_nse3000_policies(telemetry)
        
        self.processed_data.append({
            "telemetry": telemetry,
            "inference": inference,
            "timestamp": datetime.now()
        })
        
        return inference
    
    def generate_telemetry(self, sensor_id: str, data_type: str, value: float, location: Optional[str] = None):
        """Gera dados de telemetria e aplica políticas NSE3000"""
        telemetry = TelemetryData(
            sensor_id=sensor_id,
            data_type=data_type,
            value=value,
            timestamp=datetime.now(),
            location=location
        )
        
        # Aplica políticas NSE3000 após criar o objeto
        self.apply_nse3000_policies(telemetry)
        
        return telemetry
    
    def apply_nse3000_policies(self, telemetry: TelemetryData):
        """Simula aplicação de QoS e segurança NSE3000 por tipo de dado"""
        # Determina VLAN e prioridade baseado no tipo de dado
        vlan_name = "ot_network"  # VLAN para dados OT/agrícolas
        
        if telemetry.data_type in ["temperature", "actuator"]:
            priority = "high"
        elif telemetry.data_type == "image":
            priority = "medium"  # visão computacional mais tolerante a delay
        else:
            priority = "low"
        
        vlan_info = self.nse3000.vlans.get(vlan_name, {})
        vlan_id = vlan_info.get("id", "N/A")
        
        print(f"[NSE3000-QoS] Aplicando prioridade '{priority}' para {telemetry.sensor_id} "
              f"({telemetry.data_type}) via VLAN {vlan_name} (ID: {vlan_id})")
        
        self.nse3000.policies_applied += 1
    
    def _analyze_temperature(self, telemetry: TelemetryData):
        """Analisa dados de temperatura"""
        temp = telemetry.value
        if temp > 35:
            action = "ativar_irrigacao"
            alert = True
        elif temp < 10:
            action = "ativar_aquecimento"
            alert = True
        else:
            action = None
            alert = False
            
        return {
            "status": "analyzed",
            "action": action,
            "alert": alert,
            "value": temp
        }
    
    def _analyze_image(self, telemetry: TelemetryData):
        """Simula análise de visão computacional"""
        # Simulação de detecção de pragas/doenças
        detection_score = random.random()
        return {
            "status": "image_processed",
            "detection_confidence": detection_score,
            "action": "alert_agronomist" if detection_score > 0.7 else None
        }
    
    def _process_actuator_command(self, telemetry: TelemetryData):
        """Processa comando para atuador"""
        return {
            "status": "command_sent",
            "actuator_id": telemetry.sensor_id,
            "command_value": telemetry.value
        }


class SDWANManager:
    """Gerenciador SD-WAN integrado com NSE3000"""
    
    def __init__(self, nse3000: NSE3000):
        self.nse3000 = nse3000
        self.active_links = ["4G", "Satellite"]
        
    def select_link(self, telemetry: TelemetryData):
        """Seleciona melhor link SD-WAN baseado em tipo de dado e políticas NSE3000"""
        # Dados críticos (temperatura, atuadores) preferem 4G
        if telemetry.data_type in ["temperature", "actuator"]:
            selected_link = "4G"
            print(f"[SD-WAN] Link 4G selecionado para dados críticos: {telemetry.data_type}")
        # Imagens podem usar link satélite (maior latência mas maior banda)
        elif telemetry.data_type == "image":
            selected_link = "Satellite"
            print(f"[SD-WAN] Link Satellite selecionado para imagens")
        else:
            selected_link = self.active_links[0]
            print(f"[SD-WAN] Link padrão {selected_link} selecionado")
        
        # Registra uso do link no NSE3000 para estatísticas
        self.nse3000.policies_applied += 1
            
        return selected_link


def main():
    """Função principal do simulador com NSE3000 integrado"""
    print("=== Simulador de Arquitetura Híbrida com Edge Computing ===")
    print("=== Integração NSE3000 com Telemetria e SD-WAN ===\n")
    
    # Inicialização do NSE3000
    print("[Main] Inicializando NSE3000...")
    nse3000 = NSE3000()
    nse3000.configure_vlan("ot_network", 100, "high")
    nse3000.configure_vlan("sensor_network", 101, "high")
    
    # Inicialização dos componentes integrados com NSE3000
    print("\n[Main] Inicializando Edge Computing com NSE3000 integrado...")
    edge = EdgeComputing(nse3000)
    
    print("[Main] Inicializando SD-WAN Manager com NSE3000...")
    sdwan = SDWANManager(nse3000)
    
    # Simulação de processamento de telemetria
    print("\n=== Iniciando Simulação de Telemetria ===\n")
    
    # Dados de temperatura (críticos - alta prioridade)
    temp_data = TelemetryData(
        sensor_id="TEMP-001",
        data_type="temperature",
        value=38.5,
        timestamp=datetime.now(),
        location="Setor A"
    )
    sdwan.select_link(temp_data)
    edge.process_edge_inference(temp_data)
    
    # Dados de imagem (tolerante a delay - média prioridade)
    image_data = TelemetryData(
        sensor_id="CAM-002",
        data_type="image",
        value=1024.0,  # tamanho em KB
        timestamp=datetime.now(),
        location="Setor B"
    )
    sdwan.select_link(image_data)
    edge.process_edge_inference(image_data)
    
    # Comando para atuador (crítico - alta prioridade)
    actuator_data = TelemetryData(
        sensor_id="VALVE-003",
        data_type="actuator",
        value=1.0,  # abrir válvula
        timestamp=datetime.now(),
        location="Setor A"
    )
    sdwan.select_link(actuator_data)
    edge.process_edge_inference(actuator_data)
    
    # Dados genéricos (baixa prioridade)
    generic_data = TelemetryData(
        sensor_id="SENSOR-004",
        data_type="humidity",
        value=65.0,
        timestamp=datetime.now(),
        location="Setor C"
    )
    sdwan.select_link(generic_data)
    edge.process_edge_inference(generic_data)
    
    # Estatísticas finais
    print("\n=== Estatísticas NSE3000 ===")
    stats = nse3000.get_stats()
    print(f"Políticas aplicadas: {stats['policies_applied']}")
    print(f"VLANs configuradas: {stats['vlans_configured']}")
    print(f"Dados processados: {len(edge.processed_data)}")
    
    print("\n=== Simulação Concluída ===")


if __name__ == "__main__":
    main()
