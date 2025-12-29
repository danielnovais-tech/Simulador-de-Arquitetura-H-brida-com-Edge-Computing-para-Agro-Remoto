"""
Testes para EdgeNode
"""

import unittest
from simulator.edge_node import EdgeNode


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


if __name__ == '__main__':
    unittest.main()
