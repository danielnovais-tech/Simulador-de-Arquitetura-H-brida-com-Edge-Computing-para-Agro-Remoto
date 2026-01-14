"""
MQTT Telemetry System for Agriculture IoT Devices
Handles sensor data collection, processing, and distribution
"""
import json
import asyncio
import time
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import paho.mqtt.client as mqtt
from loguru import logger
from prometheus_client import Counter, Gauge, Histogram


class SensorType(Enum):
    SOIL_MOISTURE = "soil_moisture"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LIGHT = "light"
    PH_LEVEL = "ph_level"
    NUTRIENT_LEVEL = "nutrient_level"
    CROP_HEALTH = "crop_health"


@dataclass
class TelemetryData:
    sensor_id: str
    sensor_type: SensorType
    value: float
    timestamp: float
    location: Dict[str, float]
    quality: float = 1.0
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['sensor_type'] = self.sensor_type.value
        return data
    
    @staticmethod
    def from_dict(data: Dict) -> 'TelemetryData':
        data['sensor_type'] = SensorType(data['sensor_type'])
        return TelemetryData(**data)


# Prometheus metrics
messages_received = Counter('mqtt_messages_received_total', 'Total MQTT messages received', ['topic'])
messages_published = Counter('mqtt_messages_published_total', 'Total MQTT messages published', ['topic'])
message_latency = Histogram('mqtt_message_latency_seconds', 'Message processing latency')
connection_status = Gauge('mqtt_connection_status', 'MQTT connection status (1=connected, 0=disconnected)')


class MQTTTelemetrySystem:
    """
    MQTT-based telemetry system for agriculture sensor data
    """
    
    def __init__(
        self,
        broker_host: str = "localhost",
        broker_port: int = 1883,
        client_id: str = "agro_telemetry"
    ):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id
        self.client: Optional[mqtt.Client] = None
        self.connected = False
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_buffer: List[TelemetryData] = []
        self.max_buffer_size = 1000
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client = mqtt.Client(client_id=self.client_id)
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message
            
            self.client.connect(self.broker_host, self.broker_port, keepalive=60)
            self.client.loop_start()
            
            logger.info(f"Connecting to MQTT broker at {self.broker_host}:{self.broker_port}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            connection_status.set(0)
            raise
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected from MQTT broker")
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when client connects to broker"""
        if rc == 0:
            self.connected = True
            connection_status.set(1)
            logger.info("Successfully connected to MQTT broker")
            
            # Resubscribe to topics
            for topic in self.subscribers.keys():
                self.client.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")
            connection_status.set(0)
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback for when client disconnects from broker"""
        self.connected = False
        connection_status.set(0)
        logger.warning(f"Disconnected from MQTT broker with code: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Callback for when a message is received"""
        try:
            start_time = time.time()
            
            # Parse message
            payload = json.loads(msg.payload.decode())
            telemetry = TelemetryData.from_dict(payload)
            
            # Update metrics
            messages_received.labels(topic=msg.topic).inc()
            
            # Add to buffer
            self.message_buffer.append(telemetry)
            if len(self.message_buffer) > self.max_buffer_size:
                self.message_buffer.pop(0)
            
            # Call subscribers
            if msg.topic in self.subscribers:
                for callback in self.subscribers[msg.topic]:
                    callback(telemetry)
            
            # Record latency
            latency = time.time() - start_time
            message_latency.observe(latency)
            
        except Exception as e:
            logger.error(f"Error processing message from {msg.topic}: {e}")
    
    def publish(self, topic: str, telemetry: TelemetryData):
        """Publish telemetry data to a topic"""
        if not self.connected:
            logger.warning("Not connected to MQTT broker, buffering message")
            self.message_buffer.append(telemetry)
            return
        
        try:
            payload = json.dumps(telemetry.to_dict())
            self.client.publish(topic, payload, qos=1)
            messages_published.labels(topic=topic).inc()
            
        except Exception as e:
            logger.error(f"Failed to publish message to {topic}: {e}")
    
    def subscribe(self, topic: str, callback: Callable[[TelemetryData], None]):
        """Subscribe to a topic with a callback"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
            if self.connected:
                self.client.subscribe(topic)
        
        self.subscribers[topic].append(callback)
        logger.info(f"Added subscriber for topic: {topic}")
    
    def unsubscribe(self, topic: str, callback: Optional[Callable] = None):
        """Unsubscribe from a topic"""
        if topic in self.subscribers:
            if callback:
                self.subscribers[topic].remove(callback)
            else:
                del self.subscribers[topic]
                if self.connected:
                    self.client.unsubscribe(topic)
    
    def get_buffered_messages(self, sensor_type: Optional[SensorType] = None) -> List[TelemetryData]:
        """Get buffered messages, optionally filtered by sensor type"""
        if sensor_type:
            return [msg for msg in self.message_buffer if msg.sensor_type == sensor_type]
        return self.message_buffer.copy()
    
    def get_statistics(self) -> Dict:
        """Get telemetry system statistics"""
        sensor_counts = {}
        for msg in self.message_buffer:
            sensor_type = msg.sensor_type.value
            sensor_counts[sensor_type] = sensor_counts.get(sensor_type, 0) + 1
        
        return {
            "connected": self.connected,
            "broker": f"{self.broker_host}:{self.broker_port}",
            "buffered_messages": len(self.message_buffer),
            "active_subscriptions": len(self.subscribers),
            "sensor_counts": sensor_counts
        }


class TelemetryProcessor:
    """Process and validate telemetry data"""
    
    def __init__(self):
        self.validators = {
            SensorType.SOIL_MOISTURE: self._validate_soil_moisture,
            SensorType.TEMPERATURE: self._validate_temperature,
            SensorType.HUMIDITY: self._validate_humidity,
            SensorType.PH_LEVEL: self._validate_ph,
        }
    
    def validate(self, telemetry: TelemetryData) -> bool:
        """Validate telemetry data based on sensor type"""
        if telemetry.sensor_type in self.validators:
            return self.validators[telemetry.sensor_type](telemetry.value)
        return True
    
    def _validate_soil_moisture(self, value: float) -> bool:
        """Validate soil moisture (0-100%)"""
        return 0 <= value <= 100
    
    def _validate_temperature(self, value: float) -> bool:
        """Validate temperature (-40 to 60 Celsius)"""
        return -40 <= value <= 60
    
    def _validate_humidity(self, value: float) -> bool:
        """Validate humidity (0-100%)"""
        return 0 <= value <= 100
    
    def _validate_ph(self, value: float) -> bool:
        """Validate pH level (0-14)"""
        return 0 <= value <= 14
    
    def aggregate(self, telemetries: List[TelemetryData], window_seconds: float = 60) -> Dict:
        """Aggregate telemetry data over time window"""
        cutoff_time = time.time() - window_seconds
        recent = [t for t in telemetries if t.timestamp > cutoff_time]
        
        if not recent:
            return {}
        
        aggregated = {}
        for sensor_type in SensorType:
            type_data = [t.value for t in recent if t.sensor_type == sensor_type]
            if type_data:
                aggregated[sensor_type.value] = {
                    "count": len(type_data),
                    "mean": sum(type_data) / len(type_data),
                    "min": min(type_data),
                    "max": max(type_data)
                }
        
        return aggregated
