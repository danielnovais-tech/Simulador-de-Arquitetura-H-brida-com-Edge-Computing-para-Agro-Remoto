"""
Testes para EdgeNode
"""

import unittest
from simulator.edge_node import EdgeNode, simulate_edge_heartbeat


class TestEdgeNode(unittest.TestCase):
    """Testes para a classe EdgeNode"""
    
    def test_edge_node_default_power_watts(self):
        """Testa se o EdgeNode possui o valor padrão de power_watts = 12.5"""
        node = EdgeNode()
        self.assertEqual(node.power_watts, 12.5)
    
    def test_edge_node_custom_power_watts(self):
        """Testa se o EdgeNode aceita valores customizados de power_watts"""
        node = EdgeNode(power_watts=20.0)
        self.assertEqual(node.power_watts, 20.0)
    
    def test_edge_node_power_watts_type(self):
        """Testa se power_watts é do tipo float"""
        node = EdgeNode()
        self.assertIsInstance(node.power_watts, float)
    
    def test_edge_node_default_cpu_usage(self):
        """Testa se o EdgeNode possui o valor padrão de cpu_usage = 0.0"""
        node = EdgeNode()
        self.assertEqual(node.cpu_usage, 0.0)
    
    def test_edge_node_default_mem_usage(self):
        """Testa se o EdgeNode possui o valor padrão de mem_usage = 0.0"""
        node = EdgeNode()
        self.assertEqual(node.mem_usage, 0.0)
    
    def test_edge_node_custom_cpu_usage(self):
        """Testa se o EdgeNode aceita valores customizados de cpu_usage"""
        node = EdgeNode(cpu_usage=50.0)
        self.assertEqual(node.cpu_usage, 50.0)
    
    def test_edge_node_custom_mem_usage(self):
        """Testa se o EdgeNode aceita valores customizados de mem_usage"""
        node = EdgeNode(mem_usage=30.0)
        self.assertEqual(node.mem_usage, 30.0)


class TestSimulateEdgeHeartbeat(unittest.TestCase):
    """Testes para a função simulate_edge_heartbeat"""
    
    def test_heartbeat_with_zero_usage(self):
        """Testa heartbeat com CPU e memória em 0%"""
        node = EdgeNode(cpu_usage=0.0, mem_usage=0.0)
        simulate_edge_heartbeat(node)
        self.assertEqual(node.power_watts, 12.5)
    
    def test_heartbeat_with_cpu_usage(self):
        """Testa heartbeat com uso de CPU"""
        node = EdgeNode(cpu_usage=50.0, mem_usage=0.0)
        simulate_edge_heartbeat(node)
        # 12.5 + (50.0 * 0.2) + (0.0 * 0.1) = 12.5 + 10.0 + 0.0 = 22.5
        self.assertEqual(node.power_watts, 22.5)
    
    def test_heartbeat_with_mem_usage(self):
        """Testa heartbeat com uso de memória"""
        node = EdgeNode(cpu_usage=0.0, mem_usage=50.0)
        simulate_edge_heartbeat(node)
        # 12.5 + (0.0 * 0.2) + (50.0 * 0.1) = 12.5 + 0.0 + 5.0 = 17.5
        self.assertEqual(node.power_watts, 17.5)
    
    def test_heartbeat_with_both_usages(self):
        """Testa heartbeat com uso de CPU e memória"""
        node = EdgeNode(cpu_usage=50.0, mem_usage=30.0)
        simulate_edge_heartbeat(node)
        # 12.5 + (50.0 * 0.2) + (30.0 * 0.1) = 12.5 + 10.0 + 3.0 = 25.5
        self.assertEqual(node.power_watts, 25.5)
    
    def test_heartbeat_with_max_usage(self):
        """Testa heartbeat com CPU e memória em 100%"""
        node = EdgeNode(cpu_usage=100.0, mem_usage=100.0)
        simulate_edge_heartbeat(node)
        # 12.5 + (100.0 * 0.2) + (100.0 * 0.1) = 12.5 + 20.0 + 10.0 = 42.5
        self.assertEqual(node.power_watts, 42.5)
    
    def test_heartbeat_updates_existing_power(self):
        """Testa se heartbeat atualiza o power_watts existente"""
        node = EdgeNode(power_watts=50.0, cpu_usage=25.0, mem_usage=10.0)
        simulate_edge_heartbeat(node)
        # 12.5 + (25.0 * 0.2) + (10.0 * 0.1) = 12.5 + 5.0 + 1.0 = 18.5
        self.assertEqual(node.power_watts, 18.5)


if __name__ == '__main__':
    unittest.main()
