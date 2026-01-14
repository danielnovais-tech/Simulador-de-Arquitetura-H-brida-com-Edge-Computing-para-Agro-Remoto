"""
Network Resilience Manager - Implements Starlink/4G/LoRa failover
Target: <5s failover time, <50ms latency, >99.5% availability
"""
import asyncio
import time
from enum import Enum
from typing import Dict, Optional, List
from dataclasses import dataclass
from loguru import logger
import psutil
import aiohttp


class NetworkType(Enum):
    STARLINK = "starlink"
    FOURG = "4g"
    LORA = "lora"


@dataclass
class NetworkMetrics:
    latency_ms: float
    packet_loss: float
    bandwidth_mbps: float
    is_available: bool
    last_check: float


class NetworkInterface:
    """Base class for network interfaces"""
    
    def __init__(self, name: str, network_type: NetworkType, priority: int):
        self.name = name
        self.network_type = network_type
        self.priority = priority
        self.metrics = NetworkMetrics(
            latency_ms=999.0,
            packet_loss=100.0,
            bandwidth_mbps=0.0,
            is_available=False,
            last_check=0.0
        )
    
    async def health_check(self) -> bool:
        """Perform health check on the network interface"""
        raise NotImplementedError
    
    async def measure_latency(self, target: str = "8.8.8.8") -> float:
        """Measure network latency"""
        raise NotImplementedError


class StarlinkInterface(NetworkInterface):
    """Starlink satellite network interface"""
    
    def __init__(self):
        super().__init__("Starlink", NetworkType.STARLINK, priority=1)
        self.expected_latency = 40.0  # ms
    
    async def health_check(self) -> bool:
        """Check Starlink connectivity"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get('http://8.8.8.8', timeout=2) as resp:
                    latency = (time.time() - start_time) * 1000
                    self.metrics.latency_ms = latency
                    self.metrics.is_available = True
                    self.metrics.bandwidth_mbps = 150.0  # Typical Starlink
                    self.metrics.packet_loss = 0.0
                    self.metrics.last_check = time.time()
                    return True
        except Exception as e:
            logger.warning(f"Starlink health check failed: {e}")
            self.metrics.is_available = False
            self.metrics.last_check = time.time()
            return False
    
    async def measure_latency(self, target: str = "8.8.8.8") -> float:
        """Measure latency to target"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{target}', timeout=2) as resp:
                    return (time.time() - start_time) * 1000
        except:
            return 999.0


class FourGInterface(NetworkInterface):
    """4G cellular network interface"""
    
    def __init__(self):
        super().__init__("4G", NetworkType.FOURG, priority=2)
        self.expected_latency = 60.0  # ms
    
    async def health_check(self) -> bool:
        """Check 4G connectivity"""
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get('http://8.8.4.4', timeout=3) as resp:
                    latency = (time.time() - start_time) * 1000
                    self.metrics.latency_ms = latency
                    self.metrics.is_available = True
                    self.metrics.bandwidth_mbps = 50.0  # Typical 4G
                    self.metrics.packet_loss = 0.0
                    self.metrics.last_check = time.time()
                    return True
        except Exception as e:
            logger.warning(f"4G health check failed: {e}")
            self.metrics.is_available = False
            self.metrics.last_check = time.time()
            return False
    
    async def measure_latency(self, target: str = "8.8.4.4") -> float:
        """Measure latency to target"""
        start_time = time.time()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{target}', timeout=3) as resp:
                    return (time.time() - start_time) * 1000
        except:
            return 999.0


class LoRaInterface(NetworkInterface):
    """LoRa low-power wide-area network interface"""
    
    def __init__(self):
        super().__init__("LoRa", NetworkType.LORA, priority=3)
        self.expected_latency = 200.0  # ms
    
    async def health_check(self) -> bool:
        """Check LoRa connectivity - simulated"""
        # LoRa is always available as fallback but with limited bandwidth
        self.metrics.latency_ms = 180.0
        self.metrics.is_available = True
        self.metrics.bandwidth_mbps = 0.05  # Very limited
        self.metrics.packet_loss = 5.0
        self.metrics.last_check = time.time()
        return True
    
    async def measure_latency(self, target: str = "") -> float:
        """LoRa latency is relatively constant"""
        return 180.0


class NetworkResilienceManager:
    """
    Manages network failover between Starlink, 4G, and LoRa
    Target: <5s failover time
    """
    
    def __init__(self):
        self.interfaces: List[NetworkInterface] = [
            StarlinkInterface(),
            FourGInterface(),
            LoRaInterface()
        ]
        self.active_interface: Optional[NetworkInterface] = None
        self.health_check_interval = 2.0  # seconds
        self.failover_time = 0.0
        self.total_failovers = 0
        self.uptime_start = time.time()
        self.downtime_total = 0.0
        self._running = False
    
    async def start(self):
        """Start the resilience manager"""
        self._running = True
        logger.info("Starting Network Resilience Manager")
        
        # Initial failover to best available network
        await self._select_best_interface()
        
        # Start monitoring loop
        asyncio.create_task(self._monitor_loop())
    
    async def stop(self):
        """Stop the resilience manager"""
        self._running = False
        logger.info("Stopping Network Resilience Manager")
    
    async def _monitor_loop(self):
        """Continuous monitoring of network interfaces"""
        while self._running:
            await asyncio.sleep(self.health_check_interval)
            
            # Health check all interfaces
            for interface in self.interfaces:
                await interface.health_check()
            
            # Check if current interface is still healthy
            if self.active_interface and not self.active_interface.metrics.is_available:
                logger.warning(f"Active interface {self.active_interface.name} failed")
                await self._failover()
            
            # Check if better interface is available
            elif self.active_interface:
                better_interface = self._find_better_interface()
                if better_interface and better_interface.priority < self.active_interface.priority:
                    logger.info(f"Better interface {better_interface.name} available")
                    await self._failover(target=better_interface)
    
    async def _select_best_interface(self):
        """Select the best available interface"""
        # Sort by priority
        sorted_interfaces = sorted(self.interfaces, key=lambda x: x.priority)
        
        for interface in sorted_interfaces:
            if await interface.health_check():
                self.active_interface = interface
                logger.info(f"Selected {interface.name} as active interface")
                return
        
        # If no interface is available, use LoRa as last resort
        self.active_interface = self.interfaces[-1]
        logger.warning("No healthy interface found, using LoRa as fallback")
    
    def _find_better_interface(self) -> Optional[NetworkInterface]:
        """Find a better interface than current"""
        if not self.active_interface:
            return None
        
        for interface in self.interfaces:
            if (interface.priority < self.active_interface.priority and 
                interface.metrics.is_available):
                return interface
        
        return None
    
    async def _failover(self, target: Optional[NetworkInterface] = None):
        """Perform failover to target or best available interface"""
        failover_start = time.time()
        
        if target:
            self.active_interface = target
        else:
            await self._select_best_interface()
        
        self.failover_time = time.time() - failover_start
        self.total_failovers += 1
        
        logger.info(
            f"Failover completed in {self.failover_time:.3f}s to {self.active_interface.name}"
        )
        
        # Validate failover time requirement
        if self.failover_time > 5.0:
            logger.error(f"Failover time {self.failover_time:.3f}s exceeds 5s requirement!")
    
    def get_metrics(self) -> Dict:
        """Get current network metrics"""
        uptime = time.time() - self.uptime_start
        availability = ((uptime - self.downtime_total) / uptime * 100) if uptime > 0 else 0
        
        return {
            "active_interface": self.active_interface.name if self.active_interface else None,
            "active_type": self.active_interface.network_type.value if self.active_interface else None,
            "latency_ms": self.active_interface.metrics.latency_ms if self.active_interface else 999.0,
            "bandwidth_mbps": self.active_interface.metrics.bandwidth_mbps if self.active_interface else 0,
            "availability_percent": availability,
            "total_failovers": self.total_failovers,
            "last_failover_time_s": self.failover_time,
            "interfaces": {
                iface.name: {
                    "available": iface.metrics.is_available,
                    "latency_ms": iface.metrics.latency_ms,
                    "bandwidth_mbps": iface.metrics.bandwidth_mbps
                }
                for iface in self.interfaces
            }
        }
    
    async def validate_kpis(self) -> Dict[str, bool]:
        """Validate KPIs are met"""
        metrics = self.get_metrics()
        
        kpis = {
            "availability_met": metrics["availability_percent"] >= 99.5,
            "latency_met": metrics["latency_ms"] < 50.0,
            "failover_met": self.failover_time < 5.0 if self.failover_time > 0 else True
        }
        
        return kpis
