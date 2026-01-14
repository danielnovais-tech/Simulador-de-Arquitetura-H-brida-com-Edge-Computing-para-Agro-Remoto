# Quick Start Guide

## Prerequisites

- Python 3.8+
- pip

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the System

### 1. Full System Simulation

Run the complete simulation with all components:

```bash
python src/main.py
```

This will:
- Initialize network resilience (Starlink/4G/LoRa)
- Set up K3s edge cluster
- Start telemetry collection
- Run chaos engineering tests
- Display KPI results

### 2. Run Tests

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run specific test
pytest tests/unit/test_network_resilience.py -v

# Run with coverage
pytest --cov=src tests/
```

## Expected Output

```
============================================================
HYBRID EDGE COMPUTING FOR REMOTE AGRICULTURE
============================================================

System Uptime: 1.02 hours

KPI Status:
  Availability: 99.87% (target: ≥99.5%) ✓
  Latency: 42.35ms (target: <50ms) ✓
  Failover Time: 3.21s (target: <5s) ✓
  Productivity Gain: 45.67% (target: ≥30%) ✓

Chaos Engineering:
  Total Experiments: 5
  Success Rate: 100.0%

Edge Cluster:
  Healthy Nodes: 4/4
  Running Workloads: 2

Security:
  Active Sessions: 4
  Active Policies: 3

✓ ALL KPIs MET - System meets requirements!
============================================================
```

## Components

### Network Resilience
- **Starlink**: Primary (Priority 1)
- **4G**: Secondary (Priority 2)
- **LoRa**: Fallback (Priority 3)
- **Failover**: <5s automatic switching

### Edge Cluster
- **K3s**: Lightweight Kubernetes
- **Nodes**: 4 edge nodes
- **Workloads**: Telemetry processor, data aggregator

### Security
- **Zero-Trust**: All access verified
- **Encryption**: TLS/SSL certificates
- **Audit**: Complete event logging

### Monitoring
- **Prometheus**: Metrics on port 8000
- **Grafana**: Dashboard (import from config/)
- **KPIs**: Real-time tracking

## Troubleshooting

### Tests Fail
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Import Errors
```bash
# Install in development mode
pip install -e .
```

### Port Already in Use
Edit `src/observability/metrics.py` and change `prometheus_port`

## Next Steps

1. Deploy to actual edge devices
2. Configure real MQTT broker
3. Set up Prometheus/Grafana stack
4. Integrate with real sensors
5. Deploy K3s cluster

## Support

See full documentation in README.md
