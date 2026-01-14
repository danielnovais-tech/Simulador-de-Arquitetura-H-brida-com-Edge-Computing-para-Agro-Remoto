"""
K3s Edge Cluster Manager
Manages edge computing nodes and orchestration
"""
import asyncio
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass
from loguru import logger
from prometheus_client import Gauge


# Prometheus metrics
edge_nodes_total = Gauge('edge_nodes_total', 'Total number of edge nodes')
edge_nodes_healthy = Gauge('edge_nodes_healthy', 'Number of healthy edge nodes')
edge_workloads_running = Gauge('edge_workloads_running', 'Number of running workloads')


@dataclass
class EdgeNode:
    """Represents an edge computing node"""
    name: str
    node_id: str
    location: Dict[str, float]
    cpu_cores: int
    memory_gb: float
    storage_gb: float
    is_healthy: bool = True
    workloads: List[str] = None
    
    def __post_init__(self):
        if self.workloads is None:
            self.workloads = []


@dataclass
class EdgeWorkload:
    """Represents a workload running on edge"""
    name: str
    image: str
    replicas: int
    cpu_request: str
    memory_request: str
    node_selector: Optional[Dict[str, str]] = None


class K3sEdgeManager:
    """
    Manages K3s lightweight Kubernetes edge cluster
    """
    
    def __init__(self, cluster_name: str = "agro-edge-cluster"):
        self.cluster_name = cluster_name
        self.nodes: Dict[str, EdgeNode] = {}
        self.workloads: Dict[str, EdgeWorkload] = {}
        self.is_initialized = False
    
    def initialize(self, nodes: List[EdgeNode]):
        """Initialize the edge cluster with nodes"""
        for node in nodes:
            self.nodes[node.node_id] = node
        
        self.is_initialized = True
        edge_nodes_total.set(len(self.nodes))
        logger.info(f"Initialized K3s cluster with {len(self.nodes)} nodes")
    
    def add_node(self, node: EdgeNode):
        """Add a new edge node to the cluster"""
        self.nodes[node.node_id] = node
        edge_nodes_total.set(len(self.nodes))
        logger.info(f"Added edge node: {node.name}")
    
    def remove_node(self, node_id: str):
        """Remove an edge node from the cluster"""
        if node_id in self.nodes:
            node = self.nodes.pop(node_id)
            edge_nodes_total.set(len(self.nodes))
            logger.info(f"Removed edge node: {node.name}")
    
    def deploy_workload(self, workload: EdgeWorkload) -> bool:
        """Deploy a workload to the edge cluster"""
        try:
            # Find suitable nodes
            available_nodes = [n for n in self.nodes.values() if n.is_healthy]
            
            if not available_nodes:
                logger.error("No healthy nodes available for workload deployment")
                return False
            
            # Simple round-robin deployment
            for i, node in enumerate(available_nodes[:workload.replicas]):
                node.workloads.append(workload.name)
            
            self.workloads[workload.name] = workload
            edge_workloads_running.set(len(self.workloads))
            
            logger.info(f"Deployed workload: {workload.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to deploy workload {workload.name}: {e}")
            return False
    
    def remove_workload(self, workload_name: str):
        """Remove a workload from the cluster"""
        if workload_name in self.workloads:
            # Remove from all nodes
            for node in self.nodes.values():
                if workload_name in node.workloads:
                    node.workloads.remove(workload_name)
            
            del self.workloads[workload_name]
            edge_workloads_running.set(len(self.workloads))
            logger.info(f"Removed workload: {workload_name}")
    
    def update_node_health(self, node_id: str, is_healthy: bool):
        """Update node health status"""
        if node_id in self.nodes:
            self.nodes[node_id].is_healthy = is_healthy
            healthy_count = sum(1 for n in self.nodes.values() if n.is_healthy)
            edge_nodes_healthy.set(healthy_count)
            
            if not is_healthy:
                logger.warning(f"Node {self.nodes[node_id].name} marked unhealthy")
    
    def get_cluster_status(self) -> Dict:
        """Get current cluster status"""
        healthy_nodes = [n for n in self.nodes.values() if n.is_healthy]
        
        return {
            "cluster_name": self.cluster_name,
            "total_nodes": len(self.nodes),
            "healthy_nodes": len(healthy_nodes),
            "total_workloads": len(self.workloads),
            "nodes": {
                node_id: {
                    "name": node.name,
                    "healthy": node.is_healthy,
                    "workloads": len(node.workloads),
                    "location": node.location
                }
                for node_id, node in self.nodes.items()
            }
        }
    
    def generate_k3s_config(self) -> str:
        """Generate K3s cluster configuration"""
        config = {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [{
                "name": self.cluster_name,
                "cluster": {
                    "server": "https://edge-master:6443"
                }
            }],
            "contexts": [{
                "name": f"{self.cluster_name}-context",
                "context": {
                    "cluster": self.cluster_name,
                    "user": "admin"
                }
            }],
            "current-context": f"{self.cluster_name}-context"
        }
        
        return yaml.dump(config, default_flow_style=False)
    
    def generate_deployment_manifest(self, workload: EdgeWorkload) -> str:
        """Generate Kubernetes deployment manifest for a workload"""
        manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": workload.name,
                "labels": {
                    "app": workload.name,
                    "tier": "edge"
                }
            },
            "spec": {
                "replicas": workload.replicas,
                "selector": {
                    "matchLabels": {
                        "app": workload.name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": workload.name
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": workload.name,
                            "image": workload.image,
                            "resources": {
                                "requests": {
                                    "cpu": workload.cpu_request,
                                    "memory": workload.memory_request
                                }
                            }
                        }]
                    }
                }
            }
        }
        
        if workload.node_selector:
            manifest["spec"]["template"]["spec"]["nodeSelector"] = workload.node_selector
        
        return yaml.dump(manifest, default_flow_style=False)
