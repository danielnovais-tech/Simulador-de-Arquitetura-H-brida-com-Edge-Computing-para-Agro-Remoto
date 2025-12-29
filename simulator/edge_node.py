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
    """
    power_watts: float = 12.5  # valor base
