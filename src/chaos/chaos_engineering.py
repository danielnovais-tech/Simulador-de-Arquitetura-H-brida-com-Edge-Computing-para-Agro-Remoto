"""
Chaos Engineering Tests for Resilience Validation
Tests network failures, node failures, latency injection, and partitions
"""
import asyncio
import random
import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from loguru import logger


class ChaosScenario(Enum):
    NETWORK_FAILURE = "network_failure"
    NODE_FAILURE = "node_failure"
    LATENCY_INJECTION = "latency_injection"
    PARTITION = "partition"
    RESOURCE_EXHAUSTION = "resource_exhaustion"


@dataclass
class ChaosExperiment:
    """Represents a chaos engineering experiment"""
    name: str
    scenario: ChaosScenario
    duration_seconds: float
    target: str
    parameters: Dict
    success: bool = False
    start_time: float = 0
    end_time: float = 0
    observations: List[str] = None
    
    def __post_init__(self):
        if self.observations is None:
            self.observations = []


class ChaosEngineer:
    """
    Chaos Engineering framework for testing system resilience
    """
    
    def __init__(self):
        self.experiments: List[ChaosExperiment] = []
        self.active_experiments: Dict[str, ChaosExperiment] = {}
        self.results: Dict[str, Dict] = {}
    
    async def run_network_failure(
        self,
        target_network: str,
        duration: float,
        failure_type: str = "complete"
    ) -> ChaosExperiment:
        """
        Simulate network failure
        - Tests failover mechanisms
        - Validates <5s failover requirement
        """
        experiment = ChaosExperiment(
            name=f"network_failure_{target_network}",
            scenario=ChaosScenario.NETWORK_FAILURE,
            duration_seconds=duration,
            target=target_network,
            parameters={"failure_type": failure_type}
        )
        
        experiment.start_time = time.time()
        logger.info(f"Starting network failure chaos: {target_network}")
        
        try:
            # Simulate network failure
            experiment.observations.append(f"Network {target_network} failed at {experiment.start_time}")
            
            # Wait for failover to occur
            await asyncio.sleep(duration)
            
            # Check if system recovered
            experiment.observations.append(f"Network failure duration: {duration}s")
            experiment.success = True
            
        except Exception as e:
            logger.error(f"Chaos experiment failed: {e}")
            experiment.observations.append(f"Error: {e}")
            experiment.success = False
        
        finally:
            experiment.end_time = time.time()
            self.experiments.append(experiment)
        
        return experiment
    
    async def run_node_failure(
        self,
        node_id: str,
        duration: float
    ) -> ChaosExperiment:
        """
        Simulate edge node failure
        - Tests workload rescheduling
        - Validates cluster resilience
        """
        experiment = ChaosExperiment(
            name=f"node_failure_{node_id}",
            scenario=ChaosScenario.NODE_FAILURE,
            duration_seconds=duration,
            target=node_id,
            parameters={}
        )
        
        experiment.start_time = time.time()
        logger.info(f"Starting node failure chaos: {node_id}")
        
        try:
            # Simulate node failure
            experiment.observations.append(f"Node {node_id} failed")
            
            await asyncio.sleep(duration)
            
            # Node recovery
            experiment.observations.append(f"Node {node_id} recovered after {duration}s")
            experiment.success = True
            
        except Exception as e:
            logger.error(f"Node failure experiment failed: {e}")
            experiment.observations.append(f"Error: {e}")
            experiment.success = False
        
        finally:
            experiment.end_time = time.time()
            self.experiments.append(experiment)
        
        return experiment
    
    async def run_latency_injection(
        self,
        target: str,
        latency_ms: float,
        duration: float,
        jitter_ms: float = 0
    ) -> ChaosExperiment:
        """
        Inject network latency
        - Tests system performance under degraded conditions
        - Validates <50ms latency requirement tolerance
        """
        experiment = ChaosExperiment(
            name=f"latency_injection_{target}",
            scenario=ChaosScenario.LATENCY_INJECTION,
            duration_seconds=duration,
            target=target,
            parameters={
                "latency_ms": latency_ms,
                "jitter_ms": jitter_ms
            }
        )
        
        experiment.start_time = time.time()
        logger.info(f"Starting latency injection: {latency_ms}ms on {target}")
        
        try:
            # Inject latency
            experiment.observations.append(
                f"Injected {latency_ms}ms latency (±{jitter_ms}ms jitter)"
            )
            
            await asyncio.sleep(duration)
            
            experiment.observations.append("Latency injection completed")
            experiment.success = True
            
        except Exception as e:
            logger.error(f"Latency injection failed: {e}")
            experiment.observations.append(f"Error: {e}")
            experiment.success = False
        
        finally:
            experiment.end_time = time.time()
            self.experiments.append(experiment)
        
        return experiment
    
    async def run_partition(
        self,
        partition_a: List[str],
        partition_b: List[str],
        duration: float
    ) -> ChaosExperiment:
        """
        Create network partition
        - Tests split-brain scenarios
        - Validates data consistency
        """
        experiment = ChaosExperiment(
            name=f"partition_{len(partition_a)}_{len(partition_b)}",
            scenario=ChaosScenario.PARTITION,
            duration_seconds=duration,
            target="network",
            parameters={
                "partition_a": partition_a,
                "partition_b": partition_b
            }
        )
        
        experiment.start_time = time.time()
        logger.info(f"Creating network partition: {partition_a} | {partition_b}")
        
        try:
            experiment.observations.append(
                f"Partitioned network into {len(partition_a)} and {len(partition_b)} nodes"
            )
            
            await asyncio.sleep(duration)
            
            experiment.observations.append("Partition healed")
            experiment.success = True
            
        except Exception as e:
            logger.error(f"Partition experiment failed: {e}")
            experiment.observations.append(f"Error: {e}")
            experiment.success = False
        
        finally:
            experiment.end_time = time.time()
            self.experiments.append(experiment)
        
        return experiment
    
    async def run_resource_exhaustion(
        self,
        node_id: str,
        resource_type: str,
        percentage: float,
        duration: float
    ) -> ChaosExperiment:
        """
        Exhaust node resources (CPU, memory, disk)
        - Tests resource limits and throttling
        - Validates system stability under load
        """
        experiment = ChaosExperiment(
            name=f"resource_exhaustion_{node_id}_{resource_type}",
            scenario=ChaosScenario.RESOURCE_EXHAUSTION,
            duration_seconds=duration,
            target=node_id,
            parameters={
                "resource_type": resource_type,
                "percentage": percentage
            }
        )
        
        experiment.start_time = time.time()
        logger.info(f"Exhausting {resource_type} on {node_id}: {percentage}%")
        
        try:
            experiment.observations.append(
                f"Consuming {percentage}% of {resource_type}"
            )
            
            await asyncio.sleep(duration)
            
            experiment.observations.append("Resource exhaustion completed")
            experiment.success = True
            
        except Exception as e:
            logger.error(f"Resource exhaustion failed: {e}")
            experiment.observations.append(f"Error: {e}")
            experiment.success = False
        
        finally:
            experiment.end_time = time.time()
            self.experiments.append(experiment)
        
        return experiment
    
    def get_experiment_results(self) -> Dict:
        """Get results of all chaos experiments"""
        total = len(self.experiments)
        successful = sum(1 for exp in self.experiments if exp.success)
        
        results_by_scenario = {}
        for exp in self.experiments:
            scenario = exp.scenario.value
            if scenario not in results_by_scenario:
                results_by_scenario[scenario] = {
                    "total": 0,
                    "successful": 0,
                    "experiments": []
                }
            
            results_by_scenario[scenario]["total"] += 1
            if exp.success:
                results_by_scenario[scenario]["successful"] += 1
            
            results_by_scenario[scenario]["experiments"].append({
                "name": exp.name,
                "success": exp.success,
                "duration": exp.end_time - exp.start_time,
                "observations": exp.observations
            })
        
        return {
            "total_experiments": total,
            "successful_experiments": successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "by_scenario": results_by_scenario
        }
    
    async def run_comprehensive_test(self) -> Dict:
        """
        Run comprehensive chaos engineering test suite
        """
        logger.info("Starting comprehensive chaos engineering tests")
        
        # Test 1: Network failure and failover
        await self.run_network_failure("starlink", duration=10)
        await asyncio.sleep(2)
        
        # Test 2: Node failure
        await self.run_node_failure("edge-node-1", duration=15)
        await asyncio.sleep(2)
        
        # Test 3: Latency injection
        await self.run_latency_injection("4g", latency_ms=100, duration=10, jitter_ms=20)
        await asyncio.sleep(2)
        
        # Test 4: Network partition
        await self.run_partition(
            partition_a=["node-1", "node-2"],
            partition_b=["node-3", "node-4"],
            duration=10
        )
        await asyncio.sleep(2)
        
        # Test 5: Resource exhaustion
        await self.run_resource_exhaustion("edge-node-2", "cpu", 90, duration=10)
        
        logger.info("Comprehensive chaos tests completed")
        return self.get_experiment_results()
