#!/usr/bin/env python3
"""
Testes unitários para o Simulador de Arquitetura Híbrida com Edge Computing
"""

import unittest
import sys
import os

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agro_edge_simulator import EdgeNode, CloudServer, IoTSensor, AgroEdgeSimulator


class TestEdgeNode(unittest.TestCase):
    """Testes para a classe EdgeNode"""
    
    def test_initialization(self):
        """Testa inicialização do nó edge"""
        node = EdgeNode("EDGE-01", "Fazenda Norte")
        self.assertEqual(node.node_id, "EDGE-01")
        self.assertEqual(node.location, "Fazenda Norte")
        self.assertTrue(node.active)
        self.assertEqual(node.cpu_usage, 0.0)
        self.assertEqual(node.memory_usage, 0.0)
        self.assertEqual(node.data_processed, 0)
    
    def test_process_data_active(self):
        """Testa processamento de dados quando nó está ativo"""
        node = EdgeNode("EDGE-01", "Fazenda Norte")
        result = node.process_data(100)
        
        self.assertTrue(result)
        self.assertEqual(node.data_processed, 100)
        self.assertGreater(node.cpu_usage, 0)
        self.assertGreater(node.memory_usage, 0)
    
    def test_process_data_inactive(self):
        """Testa processamento de dados quando nó está inativo"""
        node = EdgeNode("EDGE-01", "Fazenda Norte")
        node.active = False
        result = node.process_data(100)
        
        self.assertFalse(result)
        self.assertEqual(node.data_processed, 0)
    
    def test_process_data_accumulation(self):
        """Testa acumulação de dados processados"""
        node = EdgeNode("EDGE-01", "Fazenda Norte")
        node.process_data(100)
        node.process_data(200)
        
        self.assertEqual(node.data_processed, 300)
    
    def test_cpu_memory_bounds(self):
        """Testa que CPU e memória não excedem 100%"""
        node = EdgeNode("EDGE-01", "Fazenda Norte")
        # Processa muitos dados para tentar exceder limites
        for _ in range(100):
            node.process_data(1000)
        
        self.assertLessEqual(node.cpu_usage, 100.0)
        self.assertGreaterEqual(node.cpu_usage, 0.0)
        self.assertLessEqual(node.memory_usage, 100.0)
        self.assertGreaterEqual(node.memory_usage, 0.0)
    
    def test_get_status(self):
        """Testa retorno de status do nó"""
        node = EdgeNode("EDGE-01", "Fazenda Norte")
        node.process_data(500)
        status = node.get_status()
        
        self.assertIn('node_id', status)
        self.assertIn('location', status)
        self.assertIn('active', status)
        self.assertIn('cpu_usage', status)
        self.assertIn('memory_usage', status)
        self.assertIn('data_processed', status)
        self.assertEqual(status['data_processed'], 500)


class TestCloudServer(unittest.TestCase):
    """Testes para a classe CloudServer"""
    
    def test_initialization(self):
        """Testa inicialização do servidor cloud"""
        cloud = CloudServer()
        self.assertEqual(cloud.total_data_received, 0)
        self.assertEqual(cloud.requests_processed, 0)
    
    def test_receive_data(self):
        """Testa recebimento de dados"""
        cloud = CloudServer()
        cloud.receive_data(100)
        
        self.assertEqual(cloud.total_data_received, 100)
        self.assertEqual(cloud.requests_processed, 1)
    
    def test_receive_data_accumulation(self):
        """Testa acumulação de dados recebidos"""
        cloud = CloudServer()
        cloud.receive_data(100)
        cloud.receive_data(200)
        cloud.receive_data(150)
        
        self.assertEqual(cloud.total_data_received, 450)
        self.assertEqual(cloud.requests_processed, 3)
    
    def test_get_status(self):
        """Testa retorno de status do servidor"""
        cloud = CloudServer()
        cloud.receive_data(100)
        status = cloud.get_status()
        
        self.assertIn('total_data_received', status)
        self.assertIn('requests_processed', status)
        self.assertEqual(status['total_data_received'], 100)
        self.assertEqual(status['requests_processed'], 1)


class TestIoTSensor(unittest.TestCase):
    """Testes para a classe IoTSensor"""
    
    def test_initialization(self):
        """Testa inicialização do sensor"""
        sensor = IoTSensor("SENSOR-001", "temperature")
        self.assertEqual(sensor.sensor_id, "SENSOR-001")
        self.assertEqual(sensor.sensor_type, "temperature")
        self.assertEqual(sensor.readings_count, 0)
    
    def test_generate_reading_temperature(self):
        """Testa geração de leitura de temperatura"""
        sensor = IoTSensor("SENSOR-001", "temperature")
        reading = sensor.generate_reading()
        
        self.assertEqual(sensor.readings_count, 1)
        self.assertIn('sensor_id', reading)
        self.assertIn('type', reading)
        self.assertIn('value', reading)
        self.assertIn('timestamp', reading)
        self.assertEqual(reading['type'], 'temperature')
        self.assertGreaterEqual(reading['value'], 15.0)
        self.assertLessEqual(reading['value'], 35.0)
    
    def test_generate_reading_humidity(self):
        """Testa geração de leitura de umidade"""
        sensor = IoTSensor("SENSOR-002", "humidity")
        reading = sensor.generate_reading()
        
        self.assertEqual(reading['type'], 'humidity')
        self.assertGreaterEqual(reading['value'], 40.0)
        self.assertLessEqual(reading['value'], 90.0)
    
    def test_generate_reading_soil_moisture(self):
        """Testa geração de leitura de umidade do solo"""
        sensor = IoTSensor("SENSOR-003", "soil_moisture")
        reading = sensor.generate_reading()
        
        self.assertEqual(reading['type'], 'soil_moisture')
        self.assertGreaterEqual(reading['value'], 20.0)
        self.assertLessEqual(reading['value'], 80.0)
    
    def test_readings_count_increment(self):
        """Testa incremento do contador de leituras"""
        sensor = IoTSensor("SENSOR-001", "temperature")
        for i in range(5):
            sensor.generate_reading()
            self.assertEqual(sensor.readings_count, i + 1)


class TestAgroEdgeSimulator(unittest.TestCase):
    """Testes para a classe AgroEdgeSimulator"""
    
    def test_initialization_defaults(self):
        """Testa inicialização com valores padrão"""
        sim = AgroEdgeSimulator()
        self.assertEqual(sim.duration, 300)
        self.assertEqual(sim.num_edges, 3)
        self.assertEqual(sim.sensors_per_edge, 3)
        self.assertEqual(len(sim.edge_nodes), 0)
        self.assertEqual(len(sim.iot_sensors), 0)
    
    def test_initialization_custom(self):
        """Testa inicialização com valores customizados"""
        sim = AgroEdgeSimulator(duration=600, num_edges=5, sensors_per_edge=4, cloud_forward_ratio=0.3)
        self.assertEqual(sim.duration, 600)
        self.assertEqual(sim.num_edges, 5)
        self.assertEqual(sim.sensors_per_edge, 4)
        self.assertEqual(sim.cloud_forward_ratio, 0.3)
    
    def test_estimate_data_size_temperature(self):
        """Testa estimativa de tamanho de dados para temperatura"""
        sim = AgroEdgeSimulator()
        sensor = IoTSensor("SENSOR-001", "temperature")
        data_size = sim._estimate_data_size(sensor)
        
        self.assertGreaterEqual(data_size, 80)
        self.assertLessEqual(data_size, 180)
    
    def test_estimate_data_size_humidity(self):
        """Testa estimativa de tamanho de dados para umidade"""
        sim = AgroEdgeSimulator()
        sensor = IoTSensor("SENSOR-002", "humidity")
        data_size = sim._estimate_data_size(sensor)
        
        self.assertGreaterEqual(data_size, 120)
        self.assertLessEqual(data_size, 220)
    
    def test_estimate_data_size_soil_moisture(self):
        """Testa estimativa de tamanho de dados para umidade do solo"""
        sim = AgroEdgeSimulator()
        sensor = IoTSensor("SENSOR-003", "soil_moisture")
        data_size = sim._estimate_data_size(sensor)
        
        self.assertGreaterEqual(data_size, 180)
        self.assertLessEqual(data_size, 320)
    
    def test_setup_creates_infrastructure(self):
        """Testa que setup cria a infraestrutura corretamente"""
        sim = AgroEdgeSimulator(num_edges=3, sensors_per_edge=2)
        # Redireciona stdout para não poluir saída dos testes
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        sim.setup()
        
        sys.stdout = old_stdout
        
        self.assertEqual(len(sim.edge_nodes), 3)
        self.assertEqual(len(sim.iot_sensors), 6)
        self.assertEqual(len(sim.sensor_to_edge_map), 6)
    
    def test_sensor_to_edge_mapping(self):
        """Testa que sensores são mapeados aos edge nodes"""
        sim = AgroEdgeSimulator(num_edges=2, sensors_per_edge=3)
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        sim.setup()
        
        sys.stdout = old_stdout
        
        # Verifica que cada sensor está mapeado a um edge node
        for sensor in sim.iot_sensors:
            self.assertIn(sensor.sensor_id, sim.sensor_to_edge_map)
            self.assertIn(sim.sensor_to_edge_map[sensor.sensor_id], sim.edge_nodes)


if __name__ == '__main__':
    unittest.main()
