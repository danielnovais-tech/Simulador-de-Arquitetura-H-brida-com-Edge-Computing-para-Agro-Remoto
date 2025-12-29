"""
Unit tests for Edge Manager (K3s)
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from edge.k3s_manager import K3sEdgeManager, EdgeNode, EdgeWorkload


def test_edge_manager_initialization():
    """Test edge manager initializes correctly"""
    manager = K3sEdgeManager(cluster_name="test-cluster")
    
    assert manager.cluster_name == "test-cluster"
    assert len(manager.nodes) == 0
    assert len(manager.workloads) == 0
    assert manager.is_initialized is False


def test_add_edge_nodes():
    """Test adding edge nodes to cluster"""
    manager = K3sEdgeManager()
    
    nodes = [
        EdgeNode(
            name="edge-1",
            node_id="node-1",
            location={"lat": 0, "lon": 0},
            cpu_cores=4,
            memory_gb=8,
            storage_gb=100
        ),
        EdgeNode(
            name="edge-2",
            node_id="node-2",
            location={"lat": 1, "lon": 1},
            cpu_cores=2,
            memory_gb=4,
            storage_gb=50
        )
    ]
    
    manager.initialize(nodes)
    
    assert manager.is_initialized is True
    assert len(manager.nodes) == 2
    assert "node-1" in manager.nodes
    assert "node-2" in manager.nodes


def test_deploy_workload():
    """Test deploying workload to edge cluster"""
    manager = K3sEdgeManager()
    
    # Add nodes
    node = EdgeNode(
        name="edge-1",
        node_id="node-1",
        location={"lat": 0, "lon": 0},
        cpu_cores=4,
        memory_gb=8,
        storage_gb=100
    )
    manager.initialize([node])
    
    # Deploy workload
    workload = EdgeWorkload(
        name="test-workload",
        image="test:latest",
        replicas=1,
        cpu_request="500m",
        memory_request="512Mi"
    )
    
    result = manager.deploy_workload(workload)
    
    assert result is True
    assert "test-workload" in manager.workloads
    assert "test-workload" in manager.nodes["node-1"].workloads


def test_node_health_update():
    """Test updating node health status"""
    manager = K3sEdgeManager()
    
    node = EdgeNode(
        name="edge-1",
        node_id="node-1",
        location={"lat": 0, "lon": 0},
        cpu_cores=4,
        memory_gb=8,
        storage_gb=100,
        is_healthy=True
    )
    manager.initialize([node])
    
    # Mark node as unhealthy
    manager.update_node_health("node-1", False)
    
    assert manager.nodes["node-1"].is_healthy is False


def test_cluster_status():
    """Test getting cluster status"""
    manager = K3sEdgeManager()
    
    nodes = [
        EdgeNode(
            name=f"edge-{i}",
            node_id=f"node-{i}",
            location={"lat": i, "lon": i},
            cpu_cores=4,
            memory_gb=8,
            storage_gb=100
        )
        for i in range(3)
    ]
    manager.initialize(nodes)
    
    status = manager.get_cluster_status()
    
    assert status["cluster_name"] == "agro-edge-cluster"
    assert status["total_nodes"] == 3
    assert status["healthy_nodes"] == 3
    assert "nodes" in status


def test_generate_deployment_manifest():
    """Test generating Kubernetes deployment manifest"""
    manager = K3sEdgeManager()
    
    workload = EdgeWorkload(
        name="telemetry",
        image="agro/telemetry:v1",
        replicas=2,
        cpu_request="500m",
        memory_request="512Mi"
    )
    
    manifest = manager.generate_deployment_manifest(workload)
    
    assert "apiVersion" in manifest
    assert "Deployment" in manifest
    assert "telemetry" in manifest
    assert "replicas: 2" in manifest
