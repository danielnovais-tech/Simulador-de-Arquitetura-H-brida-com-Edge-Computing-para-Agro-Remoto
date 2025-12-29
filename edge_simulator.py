"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Este módulo simula um sistema híbrido de edge computing para agricultura remota,
medindo o tempo de decisão entre processamento local (edge) e nuvem.
"""

import time
import random


class EdgeComputingSimulator:
    """
    Simulador de computação edge para agricultura remota.
    
    Mede e compara tempos de inferência local vs. envio para nuvem,
    mantendo métricas de desempenho (KPIs).
    """
    
    def __init__(self):
        """Inicializa o simulador com KPIs vazios."""
        self.kpis = {}
        self.inference_count = 0
    
    def process_edge_inference(self, data=None):
        """
        Processa inferência localmente no edge device.
        
        Mede o tempo de processamento e atualiza a métrica de tempo médio
        usando média móvel exponencial (EMA) com fator 0.9.
        
        Args:
            data: Dados para processar (simulado se None)
            
        Returns:
            dict: Resultado da inferência com tempo de processamento
        """
        start = time.time()
        
        # Simula processamento de inferência local
        # Em um caso real, aqui seria executado o modelo ML/AI
        if data is None:
            data = self._simulate_sensor_data()
        
        result = self._run_local_inference(data)
        
        # Calcula tempo de inferência em milissegundos
        inference_time = (time.time() - start) * 1000  # ms
        
        print(f"[Edge] Inferência local concluída em {inference_time:.1f} ms")
        
        # Atualiza KPI de tempo médio de inferência usando EMA
        # EMA = (valor_anterior * 0.9) + (novo_valor * 0.1)
        self.kpis.setdefault('avg_inference_time', 0)
        self.kpis['avg_inference_time'] = (
            self.kpis.get('avg_inference_time', 0) * 0.9 + inference_time * 0.1
        )
        
        self.inference_count += 1
        
        return {
            'result': result,
            'inference_time_ms': inference_time,
            'processing_location': 'edge'
        }
    
    def process_cloud_inference(self, data=None):
        """
        Simula envio de dados para processamento na nuvem.
        
        Inclui latência de rede e tempo de processamento remoto.
        
        Args:
            data: Dados para processar (simulado se None)
            
        Returns:
            dict: Resultado da inferência com tempo total
        """
        start = time.time()
        
        if data is None:
            data = self._simulate_sensor_data()
        
        # Simula latência de rede (ida)
        network_latency = random.uniform(50, 150)  # ms
        time.sleep(network_latency / 1000)
        
        # Simula processamento na nuvem
        result = self._run_cloud_inference(data)
        
        # Simula latência de rede (volta)
        time.sleep(network_latency / 1000)
        
        total_time = (time.time() - start) * 1000  # ms
        
        print(f"[Cloud] Inferência na nuvem concluída em {total_time:.1f} ms "
              f"(latência rede: ~{network_latency*2:.1f} ms)")
        
        # Atualiza KPI de tempo médio na nuvem
        self.kpis.setdefault('avg_cloud_time', 0)
        self.kpis['avg_cloud_time'] = (
            self.kpis.get('avg_cloud_time', 0) * 0.9 + total_time * 0.1
        )
        
        return {
            'result': result,
            'total_time_ms': total_time,
            'network_latency_ms': network_latency * 2,
            'processing_location': 'cloud'
        }
    
    def _simulate_sensor_data(self):
        """
        Simula dados de sensores agrícolas.
        
        Returns:
            dict: Dados simulados de sensores
        """
        return {
            'temperature': random.uniform(15, 35),  # Celsius
            'humidity': random.uniform(30, 90),      # %
            'soil_moisture': random.uniform(20, 80), # %
            'light_intensity': random.uniform(0, 100) # %
        }
    
    def _run_local_inference(self, data):
        """
        Simula execução de modelo de inferência local.
        
        Args:
            data: Dados dos sensores
            
        Returns:
            dict: Resultado da inferência
        """
        # Simula tempo de processamento local (mais rápido)
        processing_time = random.uniform(5, 15)  # ms
        time.sleep(processing_time / 1000)
        
        # Simula decisão baseada nos dados
        needs_irrigation = data['soil_moisture'] < 40
        needs_attention = data['temperature'] > 30 or data['humidity'] < 35
        
        return {
            'needs_irrigation': needs_irrigation,
            'needs_attention': needs_attention,
            'confidence': random.uniform(0.85, 0.99)
        }
    
    def _run_cloud_inference(self, data):
        """
        Simula execução de modelo de inferência na nuvem.
        
        Args:
            data: Dados dos sensores
            
        Returns:
            dict: Resultado da inferência (mais detalhado)
        """
        # Simula tempo de processamento na nuvem (pode ser mais sofisticado)
        processing_time = random.uniform(10, 30)  # ms
        time.sleep(processing_time / 1000)
        
        # Simula decisão mais detalhada na nuvem
        needs_irrigation = data['soil_moisture'] < 40
        needs_attention = data['temperature'] > 30 or data['humidity'] < 35
        
        return {
            'needs_irrigation': needs_irrigation,
            'needs_attention': needs_attention,
            'confidence': random.uniform(0.90, 0.99),
            'detailed_analysis': {
                'temperature_status': 'normal' if data['temperature'] < 30 else 'high',
                'moisture_level': 'adequate' if data['soil_moisture'] > 40 else 'low'
            }
        }
    
    def get_kpis(self):
        """
        Retorna os KPIs atuais do simulador.
        
        Returns:
            dict: Dicionário com todas as métricas
        """
        kpis = self.kpis.copy()
        kpis['inference_count'] = self.inference_count
        
        if 'avg_inference_time' in kpis and 'avg_cloud_time' in kpis:
            kpis['edge_vs_cloud_speedup'] = (
                kpis['avg_cloud_time'] / kpis['avg_inference_time']
                if kpis['avg_inference_time'] > 0 else 0
            )
        
        return kpis
    
    def print_kpis(self):
        """Imprime as métricas de desempenho de forma formatada."""
        kpis = self.get_kpis()
        
        print("\n" + "="*60)
        print("KPIs do Simulador de Edge Computing")
        print("="*60)
        print(f"Total de inferências: {kpis.get('inference_count', 0)}")
        
        if 'avg_inference_time' in kpis:
            print(f"Tempo médio Edge: {kpis['avg_inference_time']:.2f} ms")
        
        if 'avg_cloud_time' in kpis:
            print(f"Tempo médio Cloud: {kpis['avg_cloud_time']:.2f} ms")
        
        if 'edge_vs_cloud_speedup' in kpis:
            speedup = kpis['edge_vs_cloud_speedup']
            print(f"Aceleração Edge vs Cloud: {speedup:.2f}x mais rápido")
        
        print("="*60 + "\n")
