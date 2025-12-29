# Hybrid Edge Computing Architecture for Remote Agriculture

**Complete resilient architecture simulation with network failover, edge orchestration, telemetry, chaos testing, and observability**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Key Performance Indicators (KPIs)

This system validates and achieves the following KPIs:

- ✅ **>99.5% Availability** - High availability through network resilience
- ✅ **<5s Failover Time** - Rapid network failover between Starlink/4G/LoRa
- ✅ **<50ms Latency** - Low latency communication for real-time control
- ✅ **+30% Productivity Gain** - Autonomous harvest optimization

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Remote Agriculture Site                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Starlink    │  │     4G       │  │    LoRa      │         │
│  │  (Primary)   │  │  (Secondary) │  │  (Fallback)  │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         └────────────┬─────────────────┬─────┘                 │
│                      │                                          │
│              Network Resilience Manager                         │
│              (Auto-failover <5s)                                │
│                      │                                          │
│         ┌────────────┴────────────┐                            │
│         │                         │                            │
│    ┌────▼─────┐            ┌─────▼────┐                       │
│    │  K3s     │            │  MQTT    │                       │
│    │  Edge    │◄──────────►│ Telemetry│                       │
│    │ Cluster  │            │  Broker  │                       │
│    └────┬─────┘            └─────┬────┘                       │
│         │                         │                            │
│    ┌────▼─────────────────────────▼────┐                      │
│    │    IoT Sensors & Actuators        │                      │
│    │ (Soil, Climate, Crop Monitoring)  │                      │
│    └───────────────────────────────────┘                      │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│              Security Layer (Zero-Trust)                        │
│    NSE3000 Policies | Authentication | Encryption             │
├─────────────────────────────────────────────────────────────────┤
│           Observability (Prometheus + Grafana)                  │
│    Metrics | Logging | Alerting | Dashboards                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### 1. **Network Resilience Layer**
- **Multi-network Failover**: Automatic switching between Starlink, 4G, and LoRa
- **Health Monitoring**: Continuous health checks on all network interfaces
- **Sub-5s Failover**: Meets strict failover time requirements
- **Latency Optimization**: Maintains <50ms latency for critical operations

### 2. **Edge Computing with K3s**
- **Lightweight Kubernetes**: K3s cluster orchestration optimized for edge
- **Workload Management**: Automatic workload distribution across edge nodes
- **Resource Optimization**: Efficient CPU, memory, and storage allocation
- **High Availability**: Node failure recovery and workload rescheduling

### 3. **MQTT Telemetry System**
- **Real-time Data Collection**: Agriculture sensor data (soil, climate, crops)
- **Message Buffering**: Resilient to network interruptions
- **Data Validation**: Quality checks on sensor readings
- **Scalable Architecture**: Handles thousands of sensors

### 4. **Chaos Engineering**
- **Network Failure Simulation**: Test failover mechanisms
- **Node Failure Tests**: Validate cluster resilience
- **Latency Injection**: Performance under degraded conditions
- **Partition Testing**: Split-brain scenario validation
- **Resource Exhaustion**: Stress testing

### 5. **Observability & Monitoring**
- **Prometheus Metrics**: Real-time KPI tracking
- **Grafana Dashboards**: Visual monitoring and alerting
- **Audit Logging**: Complete system activity logs
- **Health Checks**: Component status monitoring

### 6. **Security (NSE3000 & Zero-Trust)**
- **Zero-Trust Architecture**: Never trust, always verify
- **Role-Based Access Control**: Granular permissions
- **Session Management**: Secure authentication
- **Certificate Management**: TLS/SSL encryption
- **Audit Trail**: Complete security event logging

### 7. **Agriculture Data & Validation**
- **Realistic Sensor Data**: Simulated agriculture sensor readings
- **Crop Growth Modeling**: Multi-stage crop development
- **Autonomous Harvest Decisions**: AI-driven harvest optimization
- **Productivity Metrics**: Real productivity gain calculations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

```bash
# Clone the repository
git clone https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto.git
cd Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## 🎮 Usage

### Run Full System Simulation

```bash
python src/main.py
```

This will:
1. Initialize all system components
2. Run a 60-second simulation
3. Execute chaos engineering tests
4. Display comprehensive KPI results

### Run Individual Components

```python
from network.resilience import NetworkResilienceManager
from edge.k3s_manager import K3sEdgeManager
from telemetry.mqtt_system import MQTTTelemetrySystem

# Network resilience
network_manager = NetworkResilienceManager()
await network_manager.start()
metrics = network_manager.get_metrics()

# Edge cluster management
edge_manager = K3sEdgeManager()
edge_manager.initialize(nodes)

# Telemetry system
telemetry = MQTTTelemetrySystem()
telemetry.connect()
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_network_resilience.py

# Run with coverage
pytest --cov=src tests/
```

## 📊 KPI Validation Results

After running the simulation, you'll see output like:

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

## 📁 Project Structure

```
.
├── src/
│   ├── network/          # Network resilience & failover
│   ├── edge/             # K3s edge cluster management
│   ├── telemetry/        # MQTT telemetry system
│   ├── chaos/            # Chaos engineering tests
│   ├── observability/    # Metrics & monitoring
│   ├── security/         # Zero-trust security
│   ├── agro/             # Agriculture data & validation
│   └── main.py           # Main integration system
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── config/
│   ├── k3s/              # K3s configurations
│   ├── mqtt/             # MQTT broker config
│   └── observability/    # Prometheus & Grafana configs
├── infrastructure/
│   ├── terraform/        # Infrastructure as Code
│   └── ansible/          # Configuration management
├── datasets/             # Agriculture datasets
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## 🔧 Configuration

### Network Configuration

Edit network parameters in `src/network/resilience.py`:

```python
# Health check interval (seconds)
health_check_interval = 2.0

# Session timeout (seconds)
max_session_age = 3600
```

### K3s Cluster Configuration

Kubernetes manifests in `config/k3s/`:
- Node configurations
- Deployment specs
- Service definitions

### MQTT Configuration

MQTT broker settings in `config/mqtt/mqtt-broker.yaml`:
- Broker host/port
- Authentication
- Topic structure

## 📈 Monitoring & Dashboards

### Prometheus Metrics

Available at `http://localhost:8000/metrics`

Key metrics:
- `system_availability_percent`
- `network_latency_milliseconds`
- `failover_time_seconds`
- `productivity_gain_percent`
- `edge_nodes_healthy`
- `mqtt_connection_status`

### Grafana Dashboard

Import dashboard from `config/observability/grafana-dashboard.json`

Visualizes:
- Real-time KPIs
- Network performance
- Edge cluster health
- Sensor data rates
- Error rates

## 🧪 Chaos Engineering

Run chaos tests to validate resilience:

```python
from chaos.chaos_engineering import ChaosEngineer

chaos = ChaosEngineer()

# Network failure test
await chaos.run_network_failure("starlink", duration=10)

# Node failure test
await chaos.run_node_failure("edge-node-1", duration=15)

# Latency injection
await chaos.run_latency_injection("4g", latency_ms=100, duration=10)

# Comprehensive test suite
results = await chaos.run_comprehensive_test()
```

## 🔒 Security

### Zero-Trust Principles

1. **Never Trust, Always Verify**: All access requests authenticated
2. **Least Privilege**: Minimal required permissions
3. **Microsegmentation**: Network isolation between components
4. **Continuous Monitoring**: Real-time security event logging

### Access Control

```python
from security.zero_trust import ZeroTrustSecurityManager, AccessAction

security = ZeroTrustSecurityManager()

# Check access
can_access = security.check_access(
    principal_id="edge-node-1",
    resource="sensors/zone_1",
    action=AccessAction.READ
)
```

## 🌾 Agriculture Use Cases

### Sensor Types Supported

- Soil moisture
- Soil/air temperature
- Humidity
- Light intensity
- pH levels
- Nutrient levels (N, P, K)
- Crop health monitoring

### Autonomous Harvest

System analyzes:
- Crop growth stage
- Environmental conditions
- Crop health score
- Optimal timing

Makes decisions to maximize:
- Yield quality
- Resource efficiency
- Labor optimization
- Waste reduction

## 📝 Infrastructure as Code

### Terraform (Coming Soon)

Infrastructure provisioning for:
- Cloud resources
- Network configuration
- Storage allocation

### Ansible Playbooks (Coming Soon)

Configuration management for:
- K3s cluster setup
- MQTT broker deployment
- Monitoring stack installation

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Daniel Novais** - Initial work

## 🙏 Acknowledgments

- K3s for lightweight Kubernetes
- Eclipse Mosquitto for MQTT broker
- Prometheus & Grafana for observability
- Chaos Toolkit for chaos engineering framework

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact: [GitHub Profile](https://github.com/danielnovais-tech)

---

**Built with ❤️ for sustainable and resilient agriculture technology**
