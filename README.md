# Simulador-de-Arquitetura-Híbrida-com-Edge-Computing-para-Agro-Remoto

Simula rede híbrida, edge computing resiliente e testes de validação

## Descrição

Este simulador demonstra uma arquitetura híbrida para agricultura remota, combinando:
- **Edge Computing**: Processamento local em nós distribuídos
- **Cloud Computing**: Análise agregada e armazenamento centralizado
- **Resiliência**: Capacidade de recuperação de falhas
- **Sensores IoT**: Monitoramento de múltiplos parâmetros agrícolas

## Características

- ✅ Simulação de sensores agrícolas (temperatura, umidade do solo, pH, etc.)
- ✅ Processamento distribuído em nós Edge
- ✅ Sincronização com servidor Cloud
- ✅ Detecção de alertas em tempo real
- ✅ Teste de resiliência com falhas e recuperação automática
- ✅ Analytics agregado na nuvem
- ✅ Logging estruturado com níveis de informação
- ✅ Exportação de métricas em formato JSON
- ✅ Argumentos de linha de comando configuráveis

## Como Executar

### Execução básica (padrão: 3 ciclos)
```bash
python3 agro_edge_simulator.py
```

### Execução com argumentos personalizados
```bash
# Executar com 5 ciclos
python3 agro_edge_simulator.py --cycles 5

# Executar com 10 ciclos e pausa de 1 segundo entre ciclos
python3 agro_edge_simulator.py --cycles 10 --sleep 1.0

# Ver todas as opções disponíveis
python3 agro_edge_simulator.py --help
```

### Opções de Linha de Comando

- `--cycles N`: Define o número de ciclos da simulação (padrão: 3)
- `--sleep S`: Define o tempo de pausa entre ciclos em segundos (padrão: 0.5)

### Saída de Dados

O simulador gera um arquivo `metrics.json` contendo:
- Métricas da simulação (dados gerados, processados, alertas)
- Performance dos nós Edge
- Estatísticas do Cloud Analytics
- Informações de infraestrutura

## Requisitos

- Python 3.8 ou superior
- Bibliotecas padrão do Python (sem dependências externas)

## Arquitetura

O simulador implementa uma arquitetura de três camadas:

1. **Camada de Sensores**: 15 sensores distribuídos coletando dados
2. **Camada Edge**: 3 nós de processamento local com buffer e detecção de alertas
3. **Camada Cloud**: Servidor centralizado para analytics avançado

## Tipos de Sensores Simulados

- Temperatura
- Umidade do Solo
- Umidade do Ar
- Luminosidade
- pH do Solo
- Precipitação
