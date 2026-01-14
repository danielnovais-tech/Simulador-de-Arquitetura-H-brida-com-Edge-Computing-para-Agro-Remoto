"""
EdgeNode: Nó de computação de borda para processamento local em ambientes agrícolas remotos.
"""

from dataclasses import dataclass


@dataclass
class EdgeNode:
    """
    Representa um nó de edge computing em ambiente agrícola remoto.
    
    Attributes:
        power_watts: Consumo de energia em watts. Muito relevante no agro remoto
                     onde a eficiência energética é crítica.
        cpu_usage: Percentual de uso de CPU (0-100)
        mem_usage: Percentual de uso de memória (0-100)
    """
    power_watts: float = 12.5  # valor base
    cpu_usage: float = 0.0
    mem_usage: float = 0.0


def simulate_edge_heartbeat(node: EdgeNode) -> None:
    """
    Simula heartbeat de um nó edge e atualiza o consumo de energia.
    
    O consumo de energia é calculado com base no uso de CPU e memória:
    - Base: 12.5W
    - Adicional por CPU: 0.2W por percentual de uso
    - Adicional por memória: 0.1W por percentual de uso
    
    Args:
        node: O nó EdgeNode a ter seu consumo atualizado
    """
    node.power_watts = 12.5 + (node.cpu_usage * 0.2) + (node.mem_usage * 0.1)
