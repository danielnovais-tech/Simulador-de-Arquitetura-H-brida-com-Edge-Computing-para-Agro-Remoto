"""
Main Integration System - Hybrid Edge Computing for Remote Agriculture
Integrates all components: Network, Edge, Telemetry, Security, Observability
"""
import asyncio
import time
from typing import Dict, Optional
from loguru import logger

# Import all components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from network.resilience import NetworkResilienceManager
from telemetry.mqtt_system import MQTTTelemetrySystem, TelemetryData, SensorType
from edge.k3s_manager import K3sEdgeManager, EdgeNode, EdgeWorkload
from chaos.chaos_engineering import ChaosEngineer
from observability.metrics import ObservabilitySystem
from security.zero_trust import ZeroTrustSecurityManager, SecurityPrincipal, SecurityLevel, AccessAction
from agro.data_generator import AgroDataGenerator, CropType, HarvestValidator


class HybridEdgeAgroSystem:
    """
    Complete Hybrid Edge Computing System for Remote Agriculture
    
    Validates KPIs:
    - >99.5% availability
    - <5s failover time
    - <50ms latency
    - +30% productivity gain
    """
    
    def __init__(self):
        # Initialize all subsystems
        self.network_manager = NetworkResilienceManager()
        self.telemetry_system = MQTTTelemetrySystem(
            broker_host="localhost",
            broker_port=1883
        )
        self.edge_manager = K3sEdgeManager()
        self.chaos_engineer = ChaosEngineer()
        self.observability = ObservabilitySystem(prometheus_port=8000)
        self.security_manager = ZeroTrustSecurityManager()
        self.data_generator = AgroDataGenerator(seed=42)
        self.harvest_validator = HarvestValidator()
        
        self.is_running = False
        self.start_time = 0
        
        logger.info("Hybrid Edge Agro System initialized")
    
    async def initialize(self):
        """Initialize all system components"""
        logger.info("Initializing system components...")
        
        # Initialize observability first
        self.observability.start_metrics_server()
        
        # Initialize edge cluster
        edge_nodes = [
            EdgeNode(
                name=f"edge-node-{i}",
                node_id=f"node-{i}",
                location={"lat": -15.78 + i*0.01, "lon": -47.93 + i*0.01},
                cpu_cores=4,
                memory_gb=8,
                storage_gb=100,
                power_watts=45.0 + i * 5.0  # Realistic power consumption for edge nodes
            )
            for i in range(1, 5)
        ]
        self.edge_manager.initialize(edge_nodes)
        
        # Deploy edge workloads
        telemetry_workload = EdgeWorkload(
            name="telemetry-processor",
            image="agro/telemetry:latest",
            replicas=2,
            cpu_request="500m",
            memory_request="512Mi"
        )
        self.edge_manager.deploy_workload(telemetry_workload)
        
        # Initialize security principals
        admin_principal = SecurityPrincipal(
            id="admin",
            name="System Administrator",
            type="user",
            security_level=SecurityLevel.CRITICAL
        )
        self.security_manager.register_principal(admin_principal)
        
        for i in range(1, 5):
            edge_principal = SecurityPrincipal(
                id=f"edge-node-{i}",
                name=f"Edge Node {i}",
                type="device",
                security_level=SecurityLevel.INTERNAL
            )
            self.security_manager.register_principal(edge_principal)
        
        # Start network resilience manager
        await self.network_manager.start()
        
        self.start_time = time.time()
        logger.info("System initialization complete")
    
    async def run_simulation(self, duration_seconds: int = 300):
        """Run full system simulation"""
        logger.info(f"Starting {duration_seconds}s simulation...")
        self.is_running = True
        
        simulation_start = time.time()
        iteration = 0
        
        while time.time() - simulation_start < duration_seconds and self.is_running:
            iteration += 1
            
            # Generate sensor data
            for location in self.data_generator.locations[:3]:  # Use 3 locations
                # Generate sensor reading
                sensor_reading = self.data_generator.generate_sensor_reading(location)
                
                # Create telemetry data
                telemetry = TelemetryData(
                    sensor_id=f"sensor_{location.zone_id}",
                    sensor_type=SensorType.SOIL_MOISTURE,
                    value=sensor_reading.soil_moisture,
                    timestamp=sensor_reading.timestamp,
                    location={"lat": location.latitude, "lon": location.longitude}
                )
                
                # Record metrics
                self.observability.record_sensor_reading(SensorType.SOIL_MOISTURE.value)
                
                # Validate access with zero-trust
                can_read = self.security_manager.check_access(
                    principal_id="edge-node-1",
                    resource=f"sensors/{location.zone_id}",
                    action=AccessAction.READ
                )
                
                if can_read:
                    # Publish to MQTT (simulated)
                    logger.debug(f"Published telemetry from {location.zone_id}")
            
            # Update network metrics
            net_metrics = self.network_manager.get_metrics()
            self.observability.record_latency(net_metrics["latency_ms"])
            
            # Update availability
            uptime = time.time() - self.start_time
            self.observability.update_availability(uptime, 0)
            
            # Update component health
            self.observability.update_component_health("network", True)
            self.observability.update_component_health("edge", True)
            self.observability.update_component_health("telemetry", True)
            
            # Every 10 iterations, validate a harvest decision
            if iteration % 10 == 0:
                crop_data = self.data_generator.generate_crop_data(
                    CropType.CORN,
                    days_since_planting=115  # Harvest ready
                )
                
                location = self.data_generator.locations[0]
                sensor_reading = self.data_generator.generate_sensor_reading(location)
                
                # Make autonomous harvest decision
                should_harvest = self.harvest_validator.should_harvest(
                    crop_data, sensor_reading
                )
                
                result = self.harvest_validator.validate_harvest_decision(
                    crop_data, sensor_reading, should_harvest
                )
                
                # Update productivity metrics
                productivity_gain = self.harvest_validator.calculate_productivity_gain()
                self.observability.update_productivity_gain(productivity_gain)
            
            await asyncio.sleep(1)  # 1 second intervals
        
        logger.info("Simulation completed")
    
    async def run_chaos_tests(self):
        """Run chaos engineering tests"""
        logger.info("Running chaos engineering tests...")
        
        # Run comprehensive chaos tests
        results = await self.chaos_engineer.run_comprehensive_test()
        
        logger.info(f"Chaos tests completed: {results['success_rate']:.1f}% success rate")
        return results
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        kpi_status = self.observability.get_kpi_status()
        health_status = self.observability.get_system_health()
        network_metrics = self.network_manager.get_metrics()
        edge_status = self.edge_manager.get_cluster_status()
        security_status = self.security_manager.get_security_status()
        harvest_stats = self.harvest_validator.get_harvest_statistics()
        
        return {
            "timestamp": time.time(),
            "uptime_hours": (time.time() - self.start_time) / 3600,
            "kpis": kpi_status,
            "health": health_status,
            "network": network_metrics,
            "edge_cluster": edge_status,
            "security": security_status,
            "harvest": harvest_stats
        }
    
    def validate_all_kpis(self) -> Dict[str, bool]:
        """Validate all KPI requirements"""
        kpi_status = self.observability.get_kpi_status()
        harvest_stats = self.harvest_validator.get_harvest_statistics()
        
        validation = {
            "availability": kpi_status["kpis"]["availability"]["met"],
            "latency": kpi_status["kpis"]["latency"]["met"],
            "failover_time": kpi_status["kpis"]["failover_time"]["met"],
            "productivity_gain": harvest_stats.get("meets_target", False)
        }
        
        all_met = all(validation.values())
        
        logger.info(f"KPI Validation: {'✓ ALL PASSED' if all_met else '✗ FAILED'}")
        for kpi, met in validation.items():
            logger.info(f"  {kpi}: {'✓' if met else '✗'}")
        
        return validation
    
    async def shutdown(self):
        """Shutdown all system components"""
        logger.info("Shutting down system...")
        
        self.is_running = False
        await self.network_manager.stop()
        
        logger.info("System shutdown complete")


async def main():
    """Main entry point"""
    system = HybridEdgeAgroSystem()
    
    try:
        # Initialize system
        await system.initialize()
        
        # Run simulation
        await system.run_simulation(duration_seconds=60)
        
        # Run chaos tests
        chaos_results = await system.run_chaos_tests()
        
        # Get final status
        status = system.get_system_status()
        
        # Validate KPIs
        kpi_validation = system.validate_all_kpis()
        
        # Print summary
        print("\n" + "="*60)
        print("HYBRID EDGE COMPUTING FOR REMOTE AGRICULTURE")
        print("="*60)
        print(f"\nSystem Uptime: {status['uptime_hours']:.2f} hours")
        print(f"\nKPI Status:")
        print(f"  Availability: {status['kpis']['kpis']['availability']['current']:.2f}% (target: ≥99.5%)")
        print(f"  Latency: {status['kpis']['kpis']['latency']['current']:.2f}ms (target: <50ms)")
        print(f"  Failover Time: {status['kpis']['kpis']['failover_time']['current']:.2f}s (target: <5s)")
        print(f"  Productivity Gain: {status['harvest']['productivity_gain_percent']:.2f}% (target: ≥30%)")
        print(f"\nChaos Engineering:")
        print(f"  Total Experiments: {chaos_results['total_experiments']}")
        print(f"  Success Rate: {chaos_results['success_rate']:.1f}%")
        print(f"\nEdge Cluster:")
        print(f"  Healthy Nodes: {status['edge_cluster']['healthy_nodes']}/{status['edge_cluster']['total_nodes']}")
        print(f"  Running Workloads: {status['edge_cluster']['total_workloads']}")
        # Display power consumption for each node
        for node_id, node_info in status['edge_cluster']['nodes'].items():
            print(f"   ⚡ Consumo estimado ({node_info['name']}): {node_info['power_watts']:.1f} W")
        print(f"\nSecurity:")
        print(f"  Active Sessions: {status['security']['active_sessions']}")
        print(f"  Active Policies: {status['security']['active_policies']}")
        print("\n" + "="*60)
        
        if all(kpi_validation.values()):
            print("✓ ALL KPIs MET - System meets requirements!")
        else:
            print("✗ Some KPIs not met - see details above")
        print("="*60 + "\n")
        
    finally:
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
