"""
Observability System - Metrics Collection and Monitoring
Tracks KPIs: >99.5% availability, <5s failover, <50ms latency, +30% productivity
"""
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from prometheus_client import Counter, Gauge, Histogram, Summary, start_http_server
from loguru import logger


# System-wide KPI metrics
availability_gauge = Gauge('system_availability_percent', 'System availability percentage')
failover_time_histogram = Histogram('failover_time_seconds', 'Time taken for network failover')
network_latency_histogram = Histogram('network_latency_milliseconds', 'Network latency in milliseconds')
productivity_gain_gauge = Gauge('productivity_gain_percent', 'Productivity gain percentage')

# Operational metrics
sensor_readings_total = Counter('sensor_readings_total', 'Total sensor readings processed', ['sensor_type'])
errors_total = Counter('errors_total', 'Total errors encountered', ['component', 'error_type'])
active_connections = Gauge('active_connections', 'Number of active connections', ['connection_type'])

# Performance metrics
request_duration = Summary('request_duration_seconds', 'Request duration in seconds', ['endpoint'])
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage', ['node'])
memory_usage = Gauge('memory_usage_percent', 'Memory usage percentage', ['node'])
disk_usage = Gauge('disk_usage_percent', 'Disk usage percentage', ['node'])


@dataclass
class KPIMetrics:
    """Key Performance Indicators tracking"""
    availability_percent: float = 0.0
    average_latency_ms: float = 0.0
    last_failover_time_s: float = 0.0
    productivity_gain_percent: float = 0.0
    uptime_hours: float = 0.0
    total_failovers: int = 0
    data_points_collected: int = 0


@dataclass
class SystemHealth:
    """Overall system health status"""
    is_healthy: bool = True
    components: Dict[str, bool] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    last_check: float = 0.0


class ObservabilitySystem:
    """
    Centralized observability and monitoring system
    """
    
    def __init__(self, prometheus_port: int = 8000):
        self.prometheus_port = prometheus_port
        self.kpi_metrics = KPIMetrics()
        self.system_health = SystemHealth()
        self.start_time = time.time()
        self.latency_samples: List[float] = []
        self.max_samples = 1000
        
    def start_metrics_server(self):
        """Start Prometheus metrics HTTP server"""
        try:
            start_http_server(self.prometheus_port)
            logger.info(f"Prometheus metrics server started on port {self.prometheus_port}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")
    
    def update_availability(self, uptime_seconds: float, downtime_seconds: float):
        """Update system availability metric"""
        total_time = uptime_seconds + downtime_seconds
        if total_time > 0:
            availability = (uptime_seconds / total_time) * 100
            self.kpi_metrics.availability_percent = availability
            availability_gauge.set(availability)
            
            # Check KPI threshold
            if availability < 99.5:
                self.system_health.warnings.append(
                    f"Availability {availability:.2f}% below target 99.5%"
                )
    
    def record_failover(self, failover_time_seconds: float):
        """Record network failover event"""
        self.kpi_metrics.last_failover_time_s = failover_time_seconds
        self.kpi_metrics.total_failovers += 1
        failover_time_histogram.observe(failover_time_seconds)
        
        # Check KPI threshold
        if failover_time_seconds > 5.0:
            self.system_health.errors.append(
                f"Failover time {failover_time_seconds:.2f}s exceeds 5s target"
            )
        else:
            logger.info(f"Failover completed in {failover_time_seconds:.2f}s (target: <5s)")
    
    def record_latency(self, latency_ms: float):
        """Record network latency measurement"""
        self.latency_samples.append(latency_ms)
        if len(self.latency_samples) > self.max_samples:
            self.latency_samples.pop(0)
        
        # Update average
        self.kpi_metrics.average_latency_ms = sum(self.latency_samples) / len(self.latency_samples)
        network_latency_histogram.observe(latency_ms)
        
        # Check KPI threshold
        if latency_ms > 50.0:
            self.system_health.warnings.append(
                f"Latency {latency_ms:.2f}ms exceeds 50ms target"
            )
    
    def update_productivity_gain(self, gain_percent: float):
        """Update productivity gain metric"""
        self.kpi_metrics.productivity_gain_percent = gain_percent
        productivity_gain_gauge.set(gain_percent)
        
        # Check KPI threshold
        if gain_percent < 30.0:
            self.system_health.warnings.append(
                f"Productivity gain {gain_percent:.2f}% below 30% target"
            )
    
    def record_sensor_reading(self, sensor_type: str):
        """Record sensor reading"""
        sensor_readings_total.labels(sensor_type=sensor_type).inc()
        self.kpi_metrics.data_points_collected += 1
    
    def record_error(self, component: str, error_type: str):
        """Record system error"""
        errors_total.labels(component=component, error_type=error_type).inc()
        self.system_health.errors.append(f"{component}: {error_type}")
    
    def update_component_health(self, component: str, is_healthy: bool):
        """Update health status of a system component"""
        self.system_health.components[component] = is_healthy
        self.system_health.last_check = time.time()
        
        if not is_healthy:
            logger.warning(f"Component {component} is unhealthy")
    
    def get_kpi_status(self) -> Dict:
        """Get current KPI status and validation"""
        uptime_hours = (time.time() - self.start_time) / 3600
        self.kpi_metrics.uptime_hours = uptime_hours
        
        kpi_validation = {
            "availability": {
                "current": self.kpi_metrics.availability_percent,
                "target": 99.5,
                "met": self.kpi_metrics.availability_percent >= 99.5,
                "unit": "%"
            },
            "latency": {
                "current": self.kpi_metrics.average_latency_ms,
                "target": 50.0,
                "met": self.kpi_metrics.average_latency_ms < 50.0,
                "unit": "ms"
            },
            "failover_time": {
                "current": self.kpi_metrics.last_failover_time_s,
                "target": 5.0,
                "met": self.kpi_metrics.last_failover_time_s < 5.0 if self.kpi_metrics.last_failover_time_s > 0 else True,
                "unit": "s"
            },
            "productivity_gain": {
                "current": self.kpi_metrics.productivity_gain_percent,
                "target": 30.0,
                "met": self.kpi_metrics.productivity_gain_percent >= 30.0,
                "unit": "%"
            }
        }
        
        all_kpis_met = all(kpi["met"] for kpi in kpi_validation.values())
        
        return {
            "kpis": kpi_validation,
            "all_kpis_met": all_kpis_met,
            "uptime_hours": uptime_hours,
            "total_failovers": self.kpi_metrics.total_failovers,
            "data_points_collected": self.kpi_metrics.data_points_collected
        }
    
    def get_system_health(self) -> Dict:
        """Get overall system health status"""
        healthy_components = sum(1 for h in self.system_health.components.values() if h)
        total_components = len(self.system_health.components)
        
        overall_healthy = (
            self.system_health.is_healthy and
            len(self.system_health.errors) == 0 and
            (healthy_components == total_components if total_components > 0 else True)
        )
        
        return {
            "overall_healthy": overall_healthy,
            "components": self.system_health.components,
            "healthy_components": healthy_components,
            "total_components": total_components,
            "warnings": self.system_health.warnings[-10:],  # Last 10 warnings
            "errors": self.system_health.errors[-10:],  # Last 10 errors
            "last_health_check": self.system_health.last_check
        }
    
    def generate_dashboard_config(self) -> str:
        """Generate Grafana dashboard configuration"""
        # This would generate a full Grafana dashboard JSON
        # Simplified version for demonstration
        return """
{
  "dashboard": {
    "title": "Hybrid Edge Computing - Agro Remote",
    "panels": [
      {
        "title": "System Availability",
        "targets": [{"expr": "system_availability_percent"}],
        "type": "gauge",
        "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4}
      },
      {
        "title": "Network Latency",
        "targets": [{"expr": "network_latency_milliseconds"}],
        "type": "graph",
        "gridPos": {"x": 6, "y": 0, "w": 6, "h": 4}
      },
      {
        "title": "Failover Time",
        "targets": [{"expr": "failover_time_seconds"}],
        "type": "graph",
        "gridPos": {"x": 12, "y": 0, "w": 6, "h": 4}
      },
      {
        "title": "Productivity Gain",
        "targets": [{"expr": "productivity_gain_percent"}],
        "type": "gauge",
        "gridPos": {"x": 18, "y": 0, "w": 6, "h": 4}
      },
      {
        "title": "Active Connections",
        "targets": [{"expr": "active_connections"}],
        "type": "stat",
        "gridPos": {"x": 0, "y": 4, "w": 12, "h": 4}
      },
      {
        "title": "Error Rate",
        "targets": [{"expr": "rate(errors_total[5m])"}],
        "type": "graph",
        "gridPos": {"x": 12, "y": 4, "w": 12, "h": 4}
      }
    ]
  }
}
"""
