# Simulador-de-Arquitetura-H-brida-com-Edge-Computing-para-Agro-Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador demonstra uma arquitetura híbrida de edge computing para agricultura remota, incluindo:

- Nós de edge computing distribuídos em diferentes localizações de fazendas
- Sensores IoT para monitoramento (temperatura, umidade, umidade do solo)
- Servidor cloud para processamento centralizado
- Rede híbrida com processamento distribuído e resiliente

## Uso

### Execução básica (duração padrão = 300 segundos ≈ 5 minutos)

```bash
python agro_edge_simulator.py
```

### Execução com duração personalizada

```bash
python agro_edge_simulator.py --duration 60  # 60 segundos
```

### Opções disponíveis

```bash
python agro_edge_simulator.py --help
```

## Componentes da Simulação

- **3 Nós Edge**: Processam dados localmente em diferentes fazendas
- **9 Sensores IoT**: Coletam dados de temperatura, umidade e umidade do solo
- **1 Servidor Cloud**: Recebe dados críticos para processamento centralizado
- **Arquitetura Híbrida**: Maior parte do processamento no edge, reduzindo latência e uso de rede

## Saída

O simulador fornece:

- Status em tempo real a cada 30 segundos
- Métricas de CPU e memória dos nós edge
- Estatísticas de dados processados
- Eficiência do edge computing
- Resumo final completo
