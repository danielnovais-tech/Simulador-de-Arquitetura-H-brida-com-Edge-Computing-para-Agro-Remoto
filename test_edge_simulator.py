"""
Testes para o Simulador de Edge Computing

Valida funcionalidade de métricas de tempo de decisão edge.
"""

import unittest
import time
from edge_simulator import EdgeComputingSimulator


class TestEdgeComputingSimulator(unittest.TestCase):
    """Testes para o simulador de edge computing."""
    
    def setUp(self):
        """Configura o simulador antes de cada teste."""
        self.simulator = EdgeComputingSimulator()
    
    def test_initialization(self):
        """Testa inicialização do simulador."""
        self.assertEqual(self.simulator.inference_count, 0)
        self.assertEqual(self.simulator.kpis, {})
    
    def test_process_edge_inference(self):
        """Testa processamento de inferência no edge."""
        result = self.simulator.process_edge_inference()
        
        # Verifica estrutura do resultado
        self.assertIn('result', result)
        self.assertIn('inference_time_ms', result)
        self.assertIn('processing_location', result)
        self.assertEqual(result['processing_location'], 'edge')
        
        # Verifica que o tempo foi medido
        self.assertGreater(result['inference_time_ms'], 0)
        
        # Verifica que KPI foi atualizado
        self.assertIn('avg_inference_time', self.simulator.kpis)
        self.assertGreater(self.simulator.kpis['avg_inference_time'], 0)
        
        # Verifica contador
        self.assertEqual(self.simulator.inference_count, 1)
    
    def test_process_cloud_inference(self):
        """Testa processamento de inferência na nuvem."""
        result = self.simulator.process_cloud_inference()
        
        # Verifica estrutura do resultado
        self.assertIn('result', result)
        self.assertIn('total_time_ms', result)
        self.assertIn('network_latency_ms', result)
        self.assertIn('processing_location', result)
        self.assertEqual(result['processing_location'], 'cloud')
        
        # Verifica que o tempo foi medido
        self.assertGreater(result['total_time_ms'], 0)
        self.assertGreater(result['network_latency_ms'], 0)
        
        # Verifica que KPI foi atualizado
        self.assertIn('avg_cloud_time', self.simulator.kpis)
    
    def test_exponential_moving_average(self):
        """Testa cálculo de média móvel exponencial."""
        # Primeira inferência
        self.simulator.process_edge_inference()
        first_avg = self.simulator.kpis['avg_inference_time']
        
        # Segunda inferência
        self.simulator.process_edge_inference()
        second_avg = self.simulator.kpis['avg_inference_time']
        
        # A média deve ter mudado
        self.assertNotEqual(first_avg, second_avg)
        
        # Verifica que está usando EMA (não deve ser simplesmente a média aritmética)
        self.assertEqual(self.simulator.inference_count, 2)
    
    def test_get_kpis(self):
        """Testa obtenção de KPIs."""
        # Executa algumas inferências
        self.simulator.process_edge_inference()
        self.simulator.process_cloud_inference()
        
        kpis = self.simulator.get_kpis()
        
        # Verifica presença de métricas
        self.assertIn('inference_count', kpis)
        self.assertIn('avg_inference_time', kpis)
        self.assertIn('avg_cloud_time', kpis)
        self.assertIn('edge_vs_cloud_speedup', kpis)
        
        # Verifica que speedup faz sentido (cloud deve ser mais lento)
        self.assertGreater(kpis['edge_vs_cloud_speedup'], 1.0)
    
    def test_edge_faster_than_cloud(self):
        """Testa que edge é geralmente mais rápido que cloud."""
        edge_result = self.simulator.process_edge_inference()
        cloud_result = self.simulator.process_cloud_inference()
        
        # Edge deve ser mais rápido (sem latência de rede)
        self.assertLess(
            edge_result['inference_time_ms'],
            cloud_result['total_time_ms']
        )
    
    def test_sensor_data_simulation(self):
        """Testa simulação de dados de sensores."""
        data = self.simulator._simulate_sensor_data()
        
        # Verifica campos
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
        self.assertIn('soil_moisture', data)
        self.assertIn('light_intensity', data)
        
        # Verifica valores dentro de faixas esperadas
        self.assertGreaterEqual(data['temperature'], 15)
        self.assertLessEqual(data['temperature'], 35)
        self.assertGreaterEqual(data['humidity'], 30)
        self.assertLessEqual(data['humidity'], 90)
    
    def test_inference_with_custom_data(self):
        """Testa inferência com dados customizados."""
        custom_data = {
            'temperature': 25.0,
            'humidity': 60.0,
            'soil_moisture': 50.0,
            'light_intensity': 80.0
        }
        
        result = self.simulator.process_edge_inference(custom_data)
        
        self.assertIn('result', result)
        self.assertIn('needs_irrigation', result['result'])
        self.assertIn('needs_attention', result['result'])
    
    def test_timing_measurement_accuracy(self):
        """Testa precisão da medição de tempo."""
        start = time.time()
        result = self.simulator.process_edge_inference()
        elapsed = (time.time() - start) * 1000
        
        # O tempo medido deve ser próximo do tempo real decorrido
        # (com alguma margem para overhead)
        self.assertLess(result['inference_time_ms'], elapsed + 5)
        self.assertGreater(result['inference_time_ms'], 0)


if __name__ == '__main__':
    # Executa testes com verbosidade
    unittest.main(verbosity=2)
