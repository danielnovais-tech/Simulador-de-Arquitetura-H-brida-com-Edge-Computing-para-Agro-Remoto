#!/usr/bin/env python3
"""
Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto
Simula rede híbrida, edge computing resiliente e testes de validação

Ambiente recomendado:
- Python 3.10-3.12
- Linux / macOS / Windows (WSL2 funciona bem)
- Sem dependências externas
"""

import random
import time
from typing import Dict, List, Tuple


class Sensor:
    """Representa um sensor IoT no campo"""
    
    def __init__(self, sensor_id: str, tipo: str):
        self.id = sensor_id
        self.tipo = tipo
        self.dados_coletados = 0
        self.erros = 0
        
    def coletar_dados(self) -> Dict:
        """Simula coleta de dados do sensor"""
        # Simula 5% de chance de erro
        if random.random() < 0.05:
            self.erros += 1
            return {"status": "erro", "valor": None}
        
        self.dados_coletados += 1
        if self.tipo == "temperatura":
            valor = round(random.uniform(15.0, 35.0), 2)
        elif self.tipo == "umidade":
            valor = round(random.uniform(30.0, 90.0), 2)
        elif self.tipo == "ph_solo":
            valor = round(random.uniform(5.5, 7.5), 2)
        else:
            valor = round(random.uniform(0, 100), 2)
            
        return {"status": "ok", "valor": valor, "timestamp": time.time()}


class EdgeNode:
    """Nó de processamento Edge"""
    
    CACHE_MAX_SIZE = 100  # Tamanho máximo do cache local
    
    def __init__(self, node_id: str):
        self.id = node_id
        self.sensores: List[Sensor] = []
        self.dados_processados = 0
        self.cache_local = []
        self.falhas_rede = 0
        self.online = True
        
    def adicionar_sensor(self, sensor: Sensor):
        """Adiciona sensor ao nó edge"""
        self.sensores.append(sensor)
        
    def processar_dados(self) -> List[Dict]:
        """Processa dados dos sensores localmente"""
        resultados = []
        for sensor in self.sensores:
            dado = sensor.coletar_dados()
            if dado["status"] == "ok":
                self.dados_processados += 1
                resultados.append({
                    "sensor_id": sensor.id,
                    "tipo": sensor.tipo,
                    "valor": dado["valor"],
                    "timestamp": dado["timestamp"]
                })
            
        return resultados
    
    def enviar_para_nuvem(self, dados: List[Dict]) -> Tuple[bool, List[Dict]]:
        """
        Simula envio de dados para nuvem.
        Retorna (sucesso, dados_a_enviar) onde dados_a_enviar inclui cache se online.
        """
        # Simula 10% de chance de falha de rede
        if random.random() < 0.10:
            self.falhas_rede += 1
            self.online = False
            return False, []
        
        self.online = True
        # Se online, envia dados atuais + cache acumulado
        dados_completos = self.cache_local + dados
        self.cache_local = []  # Limpa cache após envio bem-sucedido
        return True, dados_completos


class CloudServer:
    """Servidor na nuvem para processamento centralizado"""
    
    def __init__(self):
        self.dados_recebidos = 0
        self.analises_realizadas = 0
        self.alertas_gerados = 0
        
    def receber_dados(self, dados: List[Dict]):
        """Recebe dados dos nós edge"""
        self.dados_recebidos += len(dados)
        
    def analisar_tendencias(self, dados: List[Dict]):
        """Analisa tendências e gera alertas"""
        self.analises_realizadas += 1
        
        # Simula geração de alertas baseado em valores críticos
        for dado in dados:
            if dado["tipo"] == "temperatura" and dado["valor"] > 32.0:
                self.alertas_gerados += 1
            elif dado["tipo"] == "umidade" and dado["valor"] < 40.0:
                self.alertas_gerados += 1
            elif dado["tipo"] == "ph_solo" and (dado["valor"] < 6.0 or dado["valor"] > 7.0):
                self.alertas_gerados += 1


class Simulador:
    """Simulador principal da arquitetura híbrida"""
    
    def __init__(self, duration: int = 120):
        self.duration = duration
        self.edge_nodes: List[EdgeNode] = []
        self.cloud = CloudServer()
        self.ciclo_atual = 0
        self.inicio = None
        self.fim = None
        
    def configurar_infraestrutura(self, num_nodes: int = 3, sensores_por_node: int = 4):
        """Configura a infraestrutura da rede"""
        tipos_sensores = ["temperatura", "umidade", "ph_solo", "luminosidade"]
        
        for i in range(num_nodes):
            node = EdgeNode(f"edge_{i+1}")
            
            for j in range(sensores_por_node):
                tipo = tipos_sensores[j % len(tipos_sensores)]
                sensor = Sensor(f"sensor_{i+1}_{j+1}", tipo)
                node.adicionar_sensor(sensor)
                
            self.edge_nodes.append(node)
            
    def executar_ciclo(self):
        """Executa um ciclo de simulação"""
        self.ciclo_atual += 1
        
        # Cada nó edge processa seus sensores
        for node in self.edge_nodes:
            dados = node.processar_dados()
            
            # Tenta enviar para nuvem
            sucesso, dados_a_enviar = node.enviar_para_nuvem(dados)
            
            if sucesso:
                self.cloud.receber_dados(dados_a_enviar)
                self.cloud.analisar_tendencias(dados_a_enviar)
                
                # Print detalhado de cada ciclo (comentado conforme requisito)
                # print(f"  [Ciclo {self.ciclo_atual}] {node.id}: {len(dados_a_enviar)} dados enviados à nuvem")
            else:
                # Adiciona dados ao cache local para envio posterior
                node.cache_local.extend(dados)
                if len(node.cache_local) > node.CACHE_MAX_SIZE:
                    node.cache_local = node.cache_local[-node.CACHE_MAX_SIZE:]
                
                # Print de falha (comentado conforme requisito)
                # print(f"  [Ciclo {self.ciclo_atual}] {node.id}: Falha de rede - dados em cache local")
                pass
                
    def executar(self):
        """Executa a simulação completa"""
        print("=" * 80)
        print("SIMULADOR DE ARQUITETURA HÍBRIDA COM EDGE COMPUTING")
        print("Agro Remoto - Rede Resiliente")
        print("=" * 80)
        print(f"\nDuração da simulação: {self.duration} segundos")
        print(f"Nós Edge: {len(self.edge_nodes)}")
        print(f"Total de sensores: {sum(len(node.sensores) for node in self.edge_nodes)}")
        print("\nIniciando simulação...\n")
        
        self.inicio = time.time()
        tempo_decorrido = 0
        
        while tempo_decorrido < self.duration:
            self.executar_ciclo()
            
            # Print a cada 5 ciclos (mantido conforme requisito)
            if self.ciclo_atual % 5 == 0:
                nodes_online = sum(1 for node in self.edge_nodes if node.online)
                print(f"[Ciclo {self.ciclo_atual}] Status: {nodes_online}/{len(self.edge_nodes)} nós online | "
                      f"Dados na nuvem: {self.cloud.dados_recebidos} | "
                      f"Alertas: {self.cloud.alertas_gerados}")
            
            time.sleep(0.1)  # Pausa pequena entre ciclos
            tempo_decorrido = time.time() - self.inicio
            
        self.fim = time.time()
        
    def gerar_dashboard(self):
        """Gera dashboard final com estatísticas"""
        duracao_real = self.fim - self.inicio
        
        print("\n" + "=" * 80)
        print("DASHBOARD FINAL - ESTATÍSTICAS DA SIMULAÇÃO")
        print("=" * 80)
        
        print(f"\n⏱️  TEMPO DE EXECUÇÃO")
        print(f"   Duração configurada: {self.duration}s")
        print(f"   Duração real: {duracao_real:.2f}s")
        print(f"   Total de ciclos: {self.ciclo_atual}")
        
        print(f"\n📡 EDGE COMPUTING")
        total_dados_processados = sum(node.dados_processados for node in self.edge_nodes)
        total_falhas_rede = sum(node.falhas_rede for node in self.edge_nodes)
        print(f"   Nós Edge ativos: {len(self.edge_nodes)}")
        print(f"   Dados processados (edge): {total_dados_processados}")
        print(f"   Falhas de rede: {total_falhas_rede}")
        
        print(f"\n🌐 CLOUD SERVER")
        print(f"   Dados recebidos: {self.cloud.dados_recebidos}")
        print(f"   Análises realizadas: {self.cloud.analises_realizadas}")
        print(f"   Alertas gerados: {self.cloud.alertas_gerados}")
        
        print(f"\n📊 SENSORES")
        total_sensores = sum(len(node.sensores) for node in self.edge_nodes)
        total_coletas = sum(sum(s.dados_coletados for s in node.sensores) for node in self.edge_nodes)
        total_erros = sum(sum(s.erros for s in node.sensores) for node in self.edge_nodes)
        print(f"   Total de sensores: {total_sensores}")
        print(f"   Coletas bem-sucedidas: {total_coletas}")
        print(f"   Erros de sensores: {total_erros}")
        
        print(f"\n📈 KPIs")
        taxa_sucesso = (total_coletas / (total_coletas + total_erros) * 100) if (total_coletas + total_erros) > 0 else 0
        taxa_envio = (self.cloud.dados_recebidos / total_dados_processados * 100) if total_dados_processados > 0 else 0
        print(f"   Taxa de sucesso (sensores): {taxa_sucesso:.2f}%")
        print(f"   Taxa de envio à nuvem: {taxa_envio:.2f}%")
        print(f"   Resiliência (dados em cache): {total_dados_processados - self.cloud.dados_recebidos}")
        
    def gerar_relatorio(self):
        """Gera relatório detalhado por nó"""
        print("\n" + "=" * 80)
        print("RELATÓRIO DETALHADO POR NÓ EDGE")
        print("=" * 80)
        
        for node in self.edge_nodes:
            print(f"\n📍 {node.id.upper()}")
            print(f"   Status: {'🟢 Online' if node.online else '🔴 Offline'}")
            print(f"   Dados processados: {node.dados_processados}")
            print(f"   Falhas de rede: {node.falhas_rede}")
            print(f"   Cache local: {len(node.cache_local)} itens")
            print(f"   Sensores:")
            
            for sensor in node.sensores:
                status_icon = "✅" if sensor.erros == 0 else "⚠️"
                print(f"      {status_icon} {sensor.id} ({sensor.tipo}): "
                      f"{sensor.dados_coletados} leituras, {sensor.erros} erros")
        
        print("\n" + "=" * 80)


def main():
    """Função principal"""
    # Teste rápido (1-2 minutos) - configurável
    # Para simulação mais longa, aumente o valor de duration
    sim = Simulador(duration=120)  # 120 segundos = 2 minutos
    
    # Configurar infraestrutura
    sim.configurar_infraestrutura(num_nodes=3, sensores_por_node=4)
    
    # Executar simulação
    sim.executar()
    
    # Gerar dashboard e relatório final
    sim.gerar_dashboard()
    sim.gerar_relatorio()
    
    print("\n✅ Simulação concluída com sucesso!")
    print("\n💡 Dica: Para simular por menos tempo, ajuste 'duration' em main()")
    print("   Exemplo: Simulador(duration=60) para 1 minuto")
    print("\n🚀 Próximos passos: Evoluir para mini Flask + Plotly com gráficos em tempo real")


if __name__ == "__main__":
    main()
