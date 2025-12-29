"""
Unit tests for Network Resilience Manager
"""
import pytest
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from network.resilience import (
    NetworkResilienceManager,
    NetworkType,
    StarlinkInterface,
    FourGInterface,
    LoRaInterface
)


@pytest.mark.asyncio
async def test_network_manager_initialization():
    """Test network manager initializes with all interfaces"""
    manager = NetworkResilienceManager()
    
    assert len(manager.interfaces) == 3
    assert manager.active_interface is None
    assert manager.total_failovers == 0


@pytest.mark.asyncio
async def test_interface_priority():
    """Test interfaces have correct priority order"""
    manager = NetworkResilienceManager()
    
    starlink = manager.interfaces[0]
    fourg = manager.interfaces[1]
    lora = manager.interfaces[2]
    
    assert starlink.network_type == NetworkType.STARLINK
    assert starlink.priority == 1
    assert fourg.network_type == NetworkType.FOURG
    assert fourg.priority == 2
    assert lora.network_type == NetworkType.LORA
    assert lora.priority == 3


@pytest.mark.asyncio
async def test_health_check():
    """Test network health checks"""
    lora = LoRaInterface()
    
    # LoRa should always be available as fallback
    result = await lora.health_check()
    assert result is True
    assert lora.metrics.is_available is True


@pytest.mark.asyncio
async def test_metrics_collection():
    """Test network metrics are collected"""
    manager = NetworkResilienceManager()
    await manager.start()
    
    # Give it a moment to initialize
    await asyncio.sleep(0.5)
    
    metrics = manager.get_metrics()
    
    assert "active_interface" in metrics
    assert "latency_ms" in metrics
    assert "availability_percent" in metrics
    assert "interfaces" in metrics
    
    await manager.stop()


@pytest.mark.asyncio
async def test_kpi_validation():
    """Test KPI validation for network requirements"""
    manager = NetworkResilienceManager()
    await manager.start()
    
    await asyncio.sleep(0.5)
    
    kpis = await manager.validate_kpis()
    
    assert "availability_met" in kpis
    assert "latency_met" in kpis
    assert "failover_met" in kpis
    
    await manager.stop()


def test_latency_measurement():
    """Test latency measurement returns valid values"""
    lora = LoRaInterface()
    
    # LoRa has constant latency
    latency = asyncio.run(lora.measure_latency())
    assert latency > 0
    assert latency < 1000  # Should be less than 1 second
