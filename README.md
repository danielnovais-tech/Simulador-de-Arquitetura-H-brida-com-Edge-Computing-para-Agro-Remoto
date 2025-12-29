# Simulador de Arquitetura Híbrida com Edge Computing para Agro Remoto

Simula rede híbrida, edge computing resiliente e testes de validação para agricultura remota.

## Descrição

Este simulador implementa um sistema de edge computing para agricultura remota, permitindo comparar o desempenho entre processamento local (edge) e processamento na nuvem (cloud). O simulador mede o tempo de decisão para inferências locais versus envio para a nuvem.

## Características

- **Métricas de Tempo de Decisão Edge**: Mede quanto tempo leva para processar inferência local vs. enviar para nuvem
- **KPIs Automáticos**: Rastreamento de métricas de desempenho usando média móvel exponencial (EMA)
- **Simulação de Sensores**: Dados simulados de sensores agrícolas (temperatura, umidade, umidade do solo, intensidade de luz)
- **Comparação Edge vs Cloud**: Análise de desempenho entre processamento local e remoto
- **Latência de Rede Simulada**: Simula atrasos de rede realistas para comunicação com a nuvem

## Instalação

```bash
# Clone o repositório
git clone https://github.com/danielnovais-tech/Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto.git

# Entre no diretório
cd Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto

# Instale dependências (apenas Python 3.7+ necessário)
pip install -r requirements.txt
```

## Uso

### Execução Rápida

```bash
python3 demo.py
```

### Uso Programático

```python
from edge_simulator import EdgeComputingSimulator

# Cria o simulador
simulator = EdgeComputingSimulator()

# Processa inferência no edge
result = simulator.process_edge_inference()
print(f"Tempo de inferência edge: {result['inference_time_ms']:.1f} ms")

# Processa inferência na nuvem
result = simulator.process_cloud_inference()
print(f"Tempo total cloud: {result['total_time_ms']:.1f} ms")

# Visualiza KPIs
simulator.print_kpis()
```

## Exemplo de Saída

```
[Edge] Inferência local concluída em 14.7 ms
[Cloud] Inferência na nuvem concluída em 284.9 ms (latência rede: ~260.3 ms)

============================================================
KPIs do Simulador de Edge Computing
============================================================
Total de inferências: 6
Tempo médio Edge: 4.42 ms
Tempo médio Cloud: 118.23 ms
Aceleração Edge vs Cloud: 26.72x mais rápido
============================================================
```

## Métricas de Tempo de Decisão

O método `process_edge_inference` implementa a medição de tempo conforme especificado:

```python
def process_edge_inference(self):
    start = time.time()
    # ... processamento atual ...
    inference_time = (time.time() - start) * 1000  # ms
    print(f"[Edge] Inferência local concluída em {inference_time:.1f} ms")
    self.kpis.setdefault('avg_inference_time', 0)
    self.kpis['avg_inference_time'] = (
        self.kpis.get('avg_inference_time', 0) * 0.9 + inference_time * 0.1
    )
```

## Testes

Execute os testes unitários:

```bash
python3 test_edge_simulator.py
```

## Estrutura do Projeto

```
.
├── edge_simulator.py       # Módulo principal do simulador
├── demo.py                 # Demonstração de uso
├── test_edge_simulator.py  # Testes unitários
├── requirements.txt        # Dependências
└── README.md              # Esta documentação
```

## Licença

Veja o arquivo [LICENSE](LICENSE) para detalhes.
